import React, { useState } from 'react';

const CommentForm = () => {
  const [comment, setComment] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async () => {
    if (!comment.trim()) {
      setStatus('Please enter a comment');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/add_comment?text=${comment}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        setComment('');
        setStatus('Comment added successfully!');
        window.location.reload();
      } else {
        setStatus('Failed to add comment');
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <h3 className="text-lg font-bold mb-2 text-white">Add Comment</h3>
      
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        className="w-full bg-gray-700 text-white rounded-md p-2 border border-gray-600 focus:border-blue-500 focus:outline-none mb-2"
        rows="3"
        placeholder="Enter your comment here..."
      />
      
      <div className="flex justify-between items-center">
        <button
          onClick={handleSubmit}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-1 px-4 rounded-md"
        >
          Add
        </button>
        
        {status && <span className="text-sm text-gray-300">{status}</span>}
      </div>
    </div>
  );
};

export default CommentForm;