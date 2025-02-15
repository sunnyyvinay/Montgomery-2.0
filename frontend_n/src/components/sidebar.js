import React from 'react';
import {
  Box,
  VStack,
  Flex
} from '@chakra-ui/react';
import {
  EditIcon,
  InfoOutlineIcon,
  SettingsIcon,
  ChevronLeftIcon
} from '@chakra-ui/icons';
import Image from 'next/image';

function InteractiveBox({ hoverEffect, onClick, children }) {
  return (
    <Box
      position="relative"
      padding="13px"
      textAlign="start"
      borderRadius="5px"
      bg="white"
      transition="all 0.2s ease-in-out"
      _hover={hoverEffect ? {
        bg: "gray.100",
        cursor: "pointer",
        transform: "scale(1.05)",
        boxShadow: "lg",
      } : {}}
      role="group"
      onClick={onClick}  // Add click handler
    >
      {children}

      {hoverEffect && (
        <Box
          position="absolute"
          top="50%"
          right="10px"
          transform="translateY(-50%)"
          opacity={0}
          _groupHover={{ opacity: 1 }}
          transition="opacity 0.2s ease-in-out"
        >
          <Image src="/images/ex1.png" height={10} width={50} alt="example1"></Image>
        </Box>
      )}
    </Box>
  );
}

export default function SideBar({ onReset, onAutoFill }) {
  return (
    <Box
      position="fixed"
      left={0}
      top={0}
      height="100vh"
      width="25%"
      bg="white"
      p="4"
      boxShadow="md"
      zIndex={1}
    >
      {/* Header Section */}
      <Flex
        fontSize="lg"
        fontWeight="bold"
        mb="4"
        borderBottom="1px solid"
        paddingBottom="15px"
        justifyContent="space-between"
        alignItems="center"
      >

        <Box 
          overflow="hidden"
          onClick={() => window.location.reload()}
          cursor="pointer"
          >
          <Image 
            src="/images/logo.png" 
            height={70}
            width={70}
            alt="logo"
            objectFit='contain'
          />
        </Box>

        {/* Call onReset function when EditIcon is clicked */}
        <EditIcon onClick={onReset} cursor="pointer" />
      </Flex>

      {/* Content Section */}
      <VStack
        spacing="2"
        align="stretch"
        marginTop="15px"
        height="calc(100vh - 100px)"
      >
        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Integral of x^2 + 2")}>
          Integral of x<sup>2</sup> + 2
        </InteractiveBox>

        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Differentiation of e^x - x^2 + 2")}>
          Differentiation of e<sup>x</sup> - x<sup>2</sup> + 2
        </InteractiveBox>

        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Resolving 2 < x < 20")}>
          Resolving 2 {'<'} x {'<'} 20  
        </InteractiveBox>

        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Finding the value of x in x^2 + 3x - 2")}>
          Finding the value of x in x<sup>2</sup> + 3x - 2
        </InteractiveBox>

        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Drawing the graph of e^x - x^3 - 2")}>
          Drawing the graph of e<sup>x</sup> - x<sup>3</sup> - 2
        </InteractiveBox>

        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Making x the subject in y = x^3 - 2x^2")}>
          Making x the subject in y = x<sup>3</sup> - 2x<sup>2</sup>
        </InteractiveBox>

        <InteractiveBox hoverEffect={true} onClick={() => onAutoFill("Find the tangent to y = x^2 when x = 0")}>
          Find the tangent to y = x<sup>2</sup> when x = 0
        </InteractiveBox>
      </VStack>

      <Flex
        position="absolute"
        bottom="0"
        left="0"
        width="100%"
        padding="15px"
        bg="white"
        borderTop="1px solid lightgray"
        justifyContent="space-between"
        alignItems="center"
      >
        <SettingsIcon boxSize={6} />
        <InfoOutlineIcon boxSize={6} />
        <ChevronLeftIcon boxSize={6} />
      </Flex>
    </Box>
  );
}
