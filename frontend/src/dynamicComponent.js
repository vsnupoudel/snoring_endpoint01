import React, { useState, useEffect } from 'react';

const DynamicComponent = () => {
  const [htmlContent, setHtmlContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Replace the URL with your backend endpoint
    fetch('/login')
      .then(response => response.text())
      .then(data => {
        setHtmlContent(data);
        setIsLoading(false);
      })
      .catch(err => {
        setError(err);
        setIsLoading(false);
        console.error('Error fetching HTML content:', err);
      });
  }, []); // Empty dependency array ensures useEffect runs only once (on mount)

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }
  console.log(htmlContent)

  return <div dangerouslySetInnerHTML={{ __html: htmlContent }} />;
};

export default DynamicComponent;


