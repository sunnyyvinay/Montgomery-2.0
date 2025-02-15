import React, { useState } from 'react';
import { Box, Input, Button, Flex } from '@chakra-ui/react';
import axios from 'axios';

export default function UserInput({ onApiResponse, inputValue, setInputValue }) {
  const [isLoading, setIsLoading] = useState(false); // Loading state

  // Handle input change when the user types manually
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  // Handle submission for button click or Enter key press
  const handleSubmit = async () => {
    const trimmedInput = inputValue.trim();
    if (!trimmedInput) {
      alert('Please enter some text.');
      return;
    }

    setIsLoading(true); // Set loading state
    const url = 'http://localhost:8000/submit';

    try {
      console.log("Sending POST request to:", url);

      // Send user input to FastAPI and expect a video blob in response
      const response = await axios.post(url, {
        user_input: trimmedInput, // Send the trimmed input
      }, {
        responseType: 'blob'  // Expect the video blob as the response
      });

      // Convert the video blob to a URL and pass it to the parent component
      const videoBlob = new Blob([response.data], { type: 'video/mp4' });
      const videoUrl = URL.createObjectURL(videoBlob);
      console.log(videoUrl);  // Check if a valid URL is generated

      onApiResponse(videoUrl);  // Send the video URL back to the parent component
      setInputValue(''); // Clear the input field after successful submission
    } catch (error) {
      console.error('Error submitting input:', error);

      // More informative error handling:
      if (error.response) {
        alert(`Error: ${error.response.status} - ${error.response.data.detail || 'Server error'}`);
      } else if (error.request) {
        alert('Error: No response from server.');
      } else {
        alert('Error: ' + error.message);
      }
    } finally {
      setIsLoading(false); // Set loading state back to false
    }
  };

  // Handle Enter key press for form submission
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();  // Call the submit function when Enter is pressed
    }
  };

  return (
    <Box
      position="fixed"
      bottom="0"
      right="0"
      width="75%"
      height="10vh"
      bg="white"
      py={4}
      px={6}
      boxShadow="md"
    >
      <Flex width="100%" alignItems="center">
        <Box width="100%" position="relative">
          <Input
            placeholder="Enter your input"
            value={inputValue}  // Autofilled from the parent component
            onChange={handleInputChange}  // Handle manual input change
            onKeyPress={handleKeyPress}  // Add key press listener for Enter key
            size="lg"
            pr="50px"
          />
          <Button
            color="white"
            background="black"
            onClick={handleSubmit}  // Trigger submission on button click
            position="absolute"
            right="0px"
            top="50%"
            transform="translateY(-50%)"
            size="lg"
            isLoading={isLoading}  // Disable button while loading
            loadingText="Submitting"
          >
            Submit
          </Button>
        </Box>
      </Flex>
    </Box>
  );
}
