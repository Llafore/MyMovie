import { Button, ButtonText } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Heading } from '@/components/ui/heading'
import { useSignIn } from '@clerk/clerk-expo'
import { Link, useRouter } from 'expo-router'
import React from 'react'
import { Keyboard, Pressable, Text, TextInput, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
import SignInGoogleButton from '../components/SignInGoogleButton'

export default function Page() {
  const { signIn, setActive, isLoaded } = useSignIn()
  const router = useRouter();

  const [emailAddress, setEmailAddress] = React.useState('')
  const [password, setPassword] = React.useState('')

  // Handle the submission of the sign-in form
  const onSignInPress = async () => {
    if (!isLoaded) return

    // Start the sign-in process using the email and password provided
    try {
      const signInAttempt = await signIn.create({
        identifier: emailAddress,
        password,
      })

      // If sign-in process is complete, set the created session as active
      // and redirect the user
      if (signInAttempt.status === 'complete') {
        await setActive({ session: signInAttempt.createdSessionId })
        router.replace('/');
      } else {
        // If the status isn't complete, check why. User might need to
        // complete further steps.
        console.error(JSON.stringify(signInAttempt, null, 2))
      }
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }

  return (
    <SafeAreaView edges={['top']} className='flex-1 items-center justify-start p-4 bg-black'>
      <Pressable className='w-full h-full items-center justify-start gap-6' onPress={() => { Keyboard.dismiss() }}>
        <Heading size={'3xl'} className='text-white py-4'>LOGO</Heading>

        <Card size="" variant="filled" className="rounded-2xl items-center px-4 pt-4 pb-8 w-full gap-6">
          <Heading size="2xl" className="">
            Login
          </Heading>

          <SignInGoogleButton />

          <View className='flex flex-col w-full gap-2'>
            <Text className='text-white'>E-mail</Text>
            <TextInput
              className='border border-secondary-light rounded-lg p-4 w-full outline-none focus:border-primary text-white'
              autoCapitalize="none"
              value={emailAddress}
              placeholder="seuemail@email.com"
              placeholderTextColor={'#9F95A6'}
              onChangeText={(emailAddress) => setEmailAddress(emailAddress)}
            />
            <Text className='text-red-300 px-2'>Senha inválida!</Text>
          </View>

          <View className='flex flex-col w-full gap-2'>
            <Text className='text-white'>Senha</Text>
            <TextInput
              className='border border-secondary-light rounded-lg p-4 w-full outline-none focus:border-primary text-white'
              value={password}
              placeholder="Senha"
              placeholderTextColor={'#9F95A6'}
              secureTextEntry={true}
              onChangeText={(password) => setPassword(password)}
            />
            <Text className='text-white invisible'>Senha</Text>
          </View>

          <Button onPress={onSignInPress} variant='solid' action='primary' size='xl' className='w-full'>
            <ButtonText className='text-white font-bold'>Continuar</ButtonText>
          </Button>

          <View className='flex-row'>
            <Link href="/(auth)/trocar-senha" className='text-purple-300 underline'>
              Esqueci minha senha
            </Link>
          </View>
        </Card>

        <View className='flex-row'>
          <Text className='text-white'>Não possui uma conta?</Text>

          <Link href="/(auth)/cadastro">
            <Text className='text-purple-300'> Cadastre-se</Text>
          </Link>
        </View>

      </Pressable>

    </SafeAreaView>
  )
}