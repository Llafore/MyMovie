import { Link } from 'expo-router'
import { Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

export default function Page() {

  return (
      <SafeAreaView edges={['top']} className='flex-1 items-center justify-start gap-4 py-4 bg-black'>
          <View className='flex-1 items-center justify-center gap-4 py-4 bg-black'>
            <Link href="/(auth)/login">
              <Text className='text-white'>Login</Text>
            </Link>

            <Link href="/(auth)/cadastro">
              <Text className='text-white'>Cadastro</Text>
            </Link>
          </View>
      </SafeAreaView>


  )
}