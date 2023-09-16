"use client"

import { Flex, Heading } from "@chakra-ui/react";

export default function DynamicCompanyPage({ params }: { params: { company: string } }) {
    return (
      <main className="flex min-h-screen flex-col items-center">
        <Flex mt={10}>
          <Heading fontSize={'32px'} color={'#FFFFFF'}>{params.company}</Heading>
        </Flex>
        <Flex>
          
        </Flex>
      </main>
      
    )
  }
  