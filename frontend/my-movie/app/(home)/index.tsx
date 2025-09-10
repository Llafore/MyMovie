import { SignOutButton } from '@/app/components/SignOutButton'
import { Card } from '@/components/ui/card'
import { SignedIn, SignedOut, useSignIn, useUser } from '@clerk/clerk-expo'
import { Link, Redirect } from 'expo-router'
import { Suspense } from 'react'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

export default function Page() {
  const { user, } = useUser()

  console.log(user)

  return (
    <SafeAreaView edges={['top']} className='flex-1 items-center justify-start gap-4 p-4 bg-black'>
      <SignedIn>
        <View className='flex-1 items-center justify-start gap-4 bg-black w-full h-full'>
          <Text className='text-white'>Olá, {user?.emailAddresses[0].emailAddress}</Text>
          <SignOutButton />
        </View>
      </SignedIn>
      
      <SignedOut>
        <View className='flex-1 items-center justify-start gap-4 py-4 w-full h-full'>
          <View className='animate-pulse h-16 w-full bg-neutral-900' />
        </View>
      </SignedOut>
    </SafeAreaView>


  )
}
