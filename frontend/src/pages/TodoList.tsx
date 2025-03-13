import React, { useState, useEffect } from 'react';
import { todoAPI } from '../services/api';

// Define Todo type
interface Todo {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  due_date: string | null;
  created_at: string;
  updated_at: string;
  user_id: number;
}

// Define form state type
interface TodoForm {
  title: string;
  description: string;
  due_date: string;
}

const TodoList: React.FC = () => {
  // State for todos
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // State for filtering
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  
  // State for form
  const [formOpen, setFormOpen] = useState<boolean>(false);
  const [formData, setFormData] = useState<TodoForm>({
    title: '',
    description: '',
    due_date: '',
  });
  
  // State for editing
  const [editingId, setEditingId] = useState<number | null>(null);
  
  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos();
  }, []);
  
  // Fetch todos from API
  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await todoAPI.getAllTodos();
      setTodos(response.data);
    } catch (err: any) {
      setError('Failed to fetch todos. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  // Filter todos based on current filter
  const filteredTodos = todos.filter((todo) => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true; // 'all' filter
  });
  
  // Handle form input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  
  // Handle form submission (create or update)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      if (editingId) {
        // Update existing todo
        await todoAPI.updateTodo(editingId, {
          title: formData.title,
          description: formData.description || undefined,
          due_date: formData.due_date || null,
        });
      } else {
        // Create new todo
        await todoAPI.createTodo({
          title: formData.title,
          description: formData.description,
          due_date: formData.due_date,
        });
      }
      
      // Reset form and fetch updated todos
      setFormData({ title: '', description: '', due_date: '' });
      setFormOpen(false);
      setEditingId(null);
      await fetchTodos();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to save todo. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Handle todo deletion
  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }
    
    try {
      setLoading(true);
      await todoAPI.deleteTodo(id);
      await fetchTodos();
    } catch (err: any) {
      setError('Failed to delete todo. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Handle todo completion toggle
  const handleToggleComplete = async (todo: Todo) => {
    try {
      setLoading(true);
      await todoAPI.updateTodo(todo.id, {
        completed: !todo.completed,
      });
      await fetchTodos();
    } catch (err: any) {
      setError('Failed to update todo. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Handle edit button click
  const handleEdit = (todo: Todo) => {
    setFormData({
      title: todo.title,
      description: todo.description || '',
      due_date: todo.due_date || '',
    });
    setEditingId(todo.id);
    setFormOpen(true);
  };
  
  // Format date for display
  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };
  
  return (
    <div className="max-w-4xl mx-auto mt-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Todo List</h1>
        <button
          onClick={() => {
            setFormData({ title: '', description: '', due_date: '' });
            setEditingId(null);
            setFormOpen(!formOpen);
          }}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          {formOpen ? 'Cancel' : 'Add New Todo'}
        </button>
      </div>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {/* Todo Form */}
      {formOpen && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl font-semibold mb-4">
            {editingId ? 'Edit Todo' : 'Add New Todo'}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
                Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter todo title"
                required
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="description">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter description (optional)"
                rows={3}
              />
            </div>
            
            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="due_date">
                Due Date
              </label>
              <input
                type="datetime-local"
                id="due_date"
                name="due_date"
                value={formData.due_date}
                onChange={handleInputChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>
            
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${
                  loading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {loading ? 'Saving...' : 'Save Todo'}
              </button>
            </div>
          </form>
        </div>
      )}
      
      {/* Filter Tabs */}
      <div className="flex border-b mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`py-2 px-4 ${
            filter === 'all'
              ? 'border-b-2 border-blue-500 text-blue-500'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`py-2 px-4 ${
            filter === 'active'
              ? 'border-b-2 border-blue-500 text-blue-500'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Active
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`py-2 px-4 ${
            filter === 'completed'
              ? 'border-b-2 border-blue-500 text-blue-500'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Completed
        </button>
      </div>
      
      {/* Todo List */}
      {loading && !formOpen ? (
        <div className="text-center py-4">Loading todos...</div>
      ) : filteredTodos.length === 0 ? (
        <div className="text-center py-4 text-gray-500">
          {filter === 'all'
            ? 'No todos yet. Add your first todo!'
            : filter === 'active'
            ? 'No active todos.'
            : 'No completed todos.'}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTodos.map((todo) => (
            <div
              key={todo.id}
              className={`bg-white p-4 rounded-lg shadow-md ${
                todo.completed ? 'border-l-4 border-green-500' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => handleToggleComplete(todo)}
                    className="mt-1 h-5 w-5 text-blue-600"
                  />
                  <div>
                    <h3
                      className={`text-lg font-semibold ${
                        todo.completed ? 'line-through text-gray-500' : ''
                      }`}
                    >
                      {todo.title}
                    </h3>
                    {todo.description && (
                      <p className="text-gray-600 mt-1">{todo.description}</p>
                    )}
                    {todo.due_date && (
                      <p className="text-sm text-gray-500 mt-2">
                        Due: {formatDate(todo.due_date)}
                      </p>
                    )}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(todo)}
                    className="text-blue-500 hover:text-blue-700"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(todo.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TodoList;
