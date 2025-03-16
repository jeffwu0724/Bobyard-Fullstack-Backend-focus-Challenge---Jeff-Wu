'use client';

import { useState, useEffect } from 'react';

export default function CommentsPage() {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/fetch_all_comments')
      .then(response => response.json())
      .then(data => {
        if (data && data.body) {
          try {
            const parsedComments = JSON.parse(data.body);
            setComments(parsedComments);
          } catch (parseError) {
            console.error('Error parsing comments JSON:', parseError);
            setComments([]);
          }
        } else {
          setComments([]);
        }
      })
      .catch(error => console.error('Error fetching comments:', error));
  }, []);


  
  return (
    <div className="max-w-4xl mx-auto p-4 bg-gray-900">
      <h2 className="text-2xl font-bold mb-6 text-white">Comments</h2>
      
      <div className="space-y-4">
        {comments.map((comment, index) => (
          <div 
            key={comment.id || index} 
            className="bg-gray-800 rounded-lg shadow-lg overflow-hidden border border-gray-700"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 p-4">
              <div className="space-y-2">
                <div>
                  <span className="font-semibold text-white">ID: </span>
                  <span className="text-gray-300">{comment.id}</span>
                </div>
                
                <div>
                  <span className="font-semibold text-white">Author: </span>
                  <span className="text-gray-300">{comment.author}</span>
                </div>
                
                <div>
                  <span className="font-semibold text-white">Date: </span>
                  <span className="text-gray-300">{comment.date}</span>
                </div>
              </div>
              
              <div className="space-y-2">
                <div>
                  <span className="font-semibold text-white">Likes: </span>
                  <span className="text-gray-300">{comment.likes}</span>
                </div>
                
                {comment.image && (
                  <div className="mt-2">
                    <p className="font-semibold text-white mb-2">Image:</p>
                    <div className="rounded-lg border border-gray-700 inline-block">
                      <img 
                        src={comment.image} 
                        alt={`Image from ${comment.author}`}
                        className="max-w-xs object-contain h-auto"
                        style={{ maxHeight: '150px' }}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            <div className="border-t border-gray-700 p-4 bg-gray-700">
              <div>
                <p className="font-semibold text-white mb-2">Text:</p>
                <p className="text-gray-200 whitespace-pre-wrap">{comment.text}</p>
              </div>
            </div>

            <div className="mt-4 text-right">
                <button
                  onClick={() => {
                    console.log(`Comment ID: ${comment.id}`);
                    
                    // Make a fetch request to the delete endpoint
                    fetch(`http://localhost:8000/delete_comment_by_id?id=${comment.id}`)
                      .then(response => {
                        console.log('Delete response:', response);
                        
                        // Refresh the current page after successful deletion
                        if (response.ok) {
                          window.location.reload();
                        } else {
                          console.error('Failed to delete comment');
                          alert('Error deleting comment. Please try again.');
                        }
                      })
                      .catch(error => {
                        console.error('Error deleting comment:', error);
                        alert('Error deleting comment. Please try again.');
                      });
                  }}
                  className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md transition duration-300"
                >
                  Delete Comment
                </button>
              </div>
          </div>
        ))}
      </div>
    </div>
  );
}