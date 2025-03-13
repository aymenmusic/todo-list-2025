import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Home: React.FC = () => {
  const { user } = useAuth();
  
  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-center mb-6">Welcome to Todo List App</h1>
      
      <div className="text-center mb-8">
        <p className="text-lg mb-4">
          A simple and effective way to manage your tasks and stay organized.
        </p>
        <p className="text-gray-600 mb-6">
          This application allows you to create, manage, and track your todos with a clean and intuitive interface.
        </p>
      </div>
      
      <div className="flex flex-col items-center">
        {user ? (
          <div className="space-y-4 w-full max-w-md">
            <p className="text-center text-lg">
              Hello, <span className="font-semibold">{user.username}</span>! You are logged in.
            </p>
            <Link
              to="/todos"
              className="block w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-center"
            >
              Go to My Todos
            </Link>
          </div>
        ) : (
          <div className="space-y-4 w-full max-w-md">
            <p className="text-center text-lg mb-4">
              Get started by logging in or creating a new account
            </p>
            <div className="grid grid-cols-2 gap-4">
              <Link
                to="/login"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-center"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-center"
              >
                Register
              </Link>
            </div>
          </div>
        )}
      </div>
      
      <div className="mt-12 border-t pt-6">
        <h2 className="text-xl font-semibold mb-4">Features:</h2>
        <ul className="list-disc pl-6 space-y-2">
          <li>Create and manage your personal todo list</li>
          <li>Mark tasks as completed</li>
          <li>Set due dates for your tasks</li>
          <li>Secure user authentication</li>
          <li>Clean and responsive user interface</li>
        </ul>
      </div>
    </div>
  );
};

export default Home;
