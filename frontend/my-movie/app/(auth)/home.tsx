import { useUser } from '@clerk/clerk-expo'
import { Link } from 'expo-router'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

export default function Page() {
  const { user } = useUser()

  return (
      <SafeAreaView edges={['top']} className='flex-1 items-center justify-start gap-4 py-4 bg-black'>
          <Text className='text-white'>{JSON.stringify(user)}</Text>
          <View className='flex-1 items-center justify-center gap-4 py-4 bg-black'>
            <Link href="/(auth)/login">
              <Text className='text-white'>Login</Text>
            </Link>

            <Link href="/(auth)/cadastro">
              <Text className='text-blue-500'>Cadastro</Text>
            </Link>
          </View>
      </SafeAreaView>


  )
}
