import { useEffect, useState } from 'react';
import { Text, VStack, Center, Box } from '@chakra-ui/react';

const TypewriterText = () => {
  const messages = [
    "Welcome to Montgomery!",
    "Ask us any math question to start",
  ];

  const [displayedMessages, setDisplayedMessages] = useState(['', '', '']);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const typingSpeed = 50; // Speed of typing
  const pauseTime = 50; // Time to pause after each message
  const initialDelay = 1200; // 1.5-second delay before the first message

  useEffect(() => {
    // If we've displayed all the messages, stop the effect
    if (currentIndex >= messages.length) return;

    // Delay the first message by 1.5 seconds
    const delay = currentIndex === 0 && charIndex === 0 ? initialDelay : typingSpeed;

    const timer = setTimeout(() => {
      if (charIndex < messages[currentIndex].length) {
        setDisplayedMessages(prev => {
          const newMessages = [...prev];
          newMessages[currentIndex] = messages[currentIndex].substring(0, charIndex + 1);
          return newMessages;
        });
        setCharIndex(charIndex + 1);
      } else {
        setTimeout(() => {
          setCurrentIndex(currentIndex + 1);
          setCharIndex(0);
        }, pauseTime);
      }
    }, delay);

    return () => clearTimeout(timer);
  }, [currentIndex, charIndex]);

  return (
    <Center h="200px"> {/* Adjust height as needed */}
      <VStack spacing={2} align="center">
        {messages.map((_, idx) => (
          <Box key={idx} h="40px" display="flex" alignItems="center" justifyContent="center" color="white">
            <Text fontSize="xx-large" fontWeight="semibold" textAlign="center">
              {displayedMessages[idx]}
            </Text>
          </Box>
        ))}
      </VStack>
    </Center>
  );
};

export default TypewriterText;
