fetch('https://57.181.31.103:8000/')
  .then(response => response.json())
  .then(data => {
    if(data.is_using) {
      document.getElementById('true').style.display = 'block';
      document.getElementById('false').style.display = 'none';
    } else {
      document.getElementById('true').style.display = 'none';
      document.getElementById('false').style.display = 'block';
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
