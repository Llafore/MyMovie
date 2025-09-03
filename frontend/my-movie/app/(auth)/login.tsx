import { Button, ButtonSpinner, ButtonText } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Heading } from '@/components/ui/heading'
import { EyeIcon, EyeOffIcon } from '@/components/ui/icon'
import { Input, InputField, InputIcon, InputSlot } from '@/components/ui/input'
import { useSignIn } from '@clerk/clerk-expo'
import { Link, useRouter } from 'expo-router'
import React from 'react'
import { Keyboard, Pressable, Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
import SignInGoogleButton from '../components/SignInGoogleButton'

export default function Page() {
  const { signIn, setActive, isLoaded } = useSignIn()
  const router = useRouter();

  const [email, setEmail] = React.useState('')
  const [emailValido, setEmailValido] = React.useState(true)

  const [senha, setSenha] = React.useState('')
  const [mostrarSenha, setMostrarSenha] = React.useState(false)
  const [senhaValida, setSenhaValida] = React.useState(true)

  const [loading, setLoading] = React.useState(false)

  const checkEmail = (email: string) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    setEmailValido(emailRegex.test(email))
  }

  const checkSenha = (senha: string) => {
    setSenha(senha)
    const senhaRegex = /^.{8,64}$/
    setSenhaValida(senhaRegex.test(senha))
  }

  const handleState = () => {
    setMostrarSenha((state) => {
      return !state;
    });
  };
  // Handle the submission of the sign-in form
  const onEntrarPress = async () => {
    if (!emailValido || !senhaValida) return
    if (!isLoaded) return

    setLoading(true)

    // Start the sign-in process using the email and password provided
    try {
      const signInAttempt = await signIn.create({
        identifier: email,
        password: senha,
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
    } finally {
      setLoading(false)
    }
  }

  return (
    <SafeAreaView edges={['top']} className='flex-1 items-center justify-start p-4 bg-black'>
      <Pressable className='w-full h-full items-center justify-start gap-4' onPress={() => { Keyboard.dismiss() }}>
        <Heading size={'3xl'} className='text-white py-4'>LOGO</Heading>

        <Card size="" variant="filled" className="rounded-2xl items-center px-4 pt-4 pb-8 w-full gap-2">
          <Heading size="2xl" className="">
            Login
          </Heading>

          <SignInGoogleButton />

          <View className='w-full flex flex-col gap-2 pt-4 pb-6'>
            <View className='flex flex-col w-full gap-1'>
              <Text className='text-white pb-1 font-bold'>E-mail</Text>
              <Input size='xl' isInvalid={!emailValido}>
                <InputField
                  type='text'
                  value={email}
                  onBlur={() => { checkEmail(email) }}
                  onChangeText={(email) => setEmail(email)}
                  autoCapitalize='none'
                  placeholder='seuemail@emai.com' />
              </Input>

              <Text className={`text-red-300 ${emailValido ? 'invisible' : ''}`}>Email inválido</Text>

            </View>

            <View className='flex flex-col w-full gap-1'>
              <Text className='text-white pb-1 font-bold'>Senha</Text>

              <Input size='xl' isInvalid={!senhaValida}>
                <InputField
                  type={mostrarSenha ? 'text' : 'password'}
                  value={senha}
                  onChangeText={(senha) => checkSenha(senha)}
                  autoCapitalize='none'
                  placeholder='seuemail@emai.com' />

                <InputSlot className="pr-4" onPress={handleState}>
                  <InputIcon as={mostrarSenha ? EyeIcon : EyeOffIcon} />
                </InputSlot>
              </Input>

              <Text className={`text-red-300 ${senhaValida ? 'invisible' : ''}`}>Senha inválida</Text>

            </View>
          </View>

          <Button onPress={onEntrarPress} variant='solid' action='primary' size='xl' className='w-full transition disabled:bg-primary-black'>
            <ButtonSpinner className={loading ? 'data-[active=true]:text-neutral-100' : 'hidden'} color='white' ></ButtonSpinner>
            <ButtonText className='text-white font-bold pl-4 data-[disabled=true]:text-neutral-500'>Continuar</ButtonText>
          </Button>

          <View className='flex-row pt-4'>
            <Link href="/(auth)/trocar-senha" className='text-primary-light underline'>
              Esqueci minha senha
            </Link>
          </View>
        </Card>

        <View className='flex-row'>
          <Text className='text-white'>Não possui uma conta?</Text>

          <Link href="/(auth)/cadastro">
            <Text className='text-primary-light'> Cadastre-se</Text>
          </Link>
        </View>

      </Pressable>

    </SafeAreaView>
  )
}