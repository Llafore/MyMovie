import { SignOutButton } from '@/app/components/SignOutButton'
import { SignedIn, SignedOut, useUser } from '@clerk/clerk-expo'
import { Link, Redirect } from 'expo-router'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

export default function Page() {
  const { user } = useUser()

  console.log(user)

  return (
      <SafeAreaView edges={['top']} className='flex-1 items-center justify-start gap-4 py-4 bg-black'>
        <SignedIn >
          <View className='flex-1 items-center justify-start gap-4 py-4 bg-black'>
            <Text className='text-white'>Olá, {user?.emailAddresses[0].emailAddress}</Text>
            <SignOutButton />
          </View>
        </SignedIn>
        
        <SignedOut>
          {/* <Redirect href='/(auth)/home' /> */}
          <Text className='text-white'>Carregando......</Text>
        </SignedOut>
      </SafeAreaView>


  )
}
