import { Button, ButtonSpinner, ButtonText } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Heading } from '@/components/ui/heading'
import { EyeIcon, EyeOffIcon } from '@/components/ui/icon'
import { Input, InputField, InputIcon, InputSlot } from '@/components/ui/input'
import { useSignUp } from '@clerk/clerk-expo'
import { Link, useRouter } from 'expo-router'
import * as React from 'react'
import { Keyboard, Pressable, Text, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
import SignInGoogleButton from '../components/SignInGoogleButton'

export default function Cadastro() {
  const { isLoaded, signUp, setActive } = useSignUp()
  const router = useRouter();

  const [emailAddress, setEmailAddress] = React.useState('')
  const [emailValido, setEmailValido] = React.useState(true)

  const [password, setPassword] = React.useState('')
  const [mostrarSenha, setMostrarSenha] = React.useState(false)
  const [senhaValida, setSenhaValida] = React.useState(true)

  const [pendingVerification, setPendingVerification] = React.useState(false)
  const [code, setCode] = React.useState('')

  const [loading, setLoading] = React.useState(false)

  const checkEmail = (email: string) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    setEmailValido(emailRegex.test(email))
  }

  const checkSenha = (senha: string) => {
    setPassword(senha)
    const senhaRegex = /^.{8,64}$/
    setSenhaValida(senhaRegex.test(senha))
  }

  const handleState = () => {
    setMostrarSenha((state) => {
      return !state;
    });
  };

  // Handle submission of sign-up form
  const onSignUpPress = async () => {
    if (!isLoaded) return
    setLoading(true)

    // Start sign-up process using email and password provided
    try {
      await signUp.create({
        emailAddress,
        password,
      })

      // Send user an email with verification code
      await signUp.prepareEmailAddressVerification({ strategy: 'email_code' })

      // Set 'pendingVerification' to true to display second form
      // and capture OTP code
      setPendingVerification(true)
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    } finally {
      setLoading(false)
    }
  }

  // Handle submission of verification form
  const onVerifyPress = async () => {
    if (!isLoaded) return
    setLoading(true)

    try {
      // Use the code the user provided to attempt verification
      const signUpAttempt = await signUp.attemptEmailAddressVerification({
        code,
      })

      // If verification was completed, set the session to active
      // and redirect the user
      if (signUpAttempt.status === 'complete') {
        await setActive({ session: signUpAttempt.createdSessionId })
        router.replace('/')
      } else {
        // If the status is not complete, check why. User may need to
        // complete further steps.
        console.error(JSON.stringify(signUpAttempt, null, 2))
      }
    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    } finally {
      setLoading(false)
    }
  }

  if (pendingVerification) {
    return (
      <SafeAreaView edges={['top']} className='flex-1 items-center justify-start p-4 bg-black'>
        <Pressable className='w-full h-full items-center justify-start gap-4' onPress={() => { Keyboard.dismiss() }}>
          <Heading size={'2xl'} className='text-white py-2'>Verificar e-mail</Heading>

          <View className="rounded-2xl items-center px-4 pt-2 pb-8 w-full gap-8">
            <View className='flex flex-col w-full gap-1'>

              <Text className='text-white pb-1 font-bold'>Código de verificação</Text>

              <Input size='xl' isInvalid={!emailValido}>
                <InputField
                  autoCapitalize="none"
                  value={code}
                  placeholder="Digite o seu código de verificação"
                  onChangeText={(code) => setCode(code)}
                  type='text'
                />
              </Input>
            </View>

            <Button onPress={onVerifyPress} variant='solid' action='primary' size='xl' className='w-full transition disabled:bg-primary-black'>
              <ButtonSpinner className={loading ? 'data-[active=true]:text-neutral-100' : 'hidden'} color='white'></ButtonSpinner>
              <ButtonText className='text-white font-bold pl-4 data-[disabled=true]:text-neutral-500'>Verificar</ButtonText>
            </Button>
          </View>

        </Pressable>
      </SafeAreaView>
    )
  }

  return (
    <><SafeAreaView edges={['top']} className='flex-1 items-center justify-start p-4 bg-black'>
      <Pressable className='w-full h-full items-center justify-start gap-4' onPress={() => { Keyboard.dismiss() }}>
        <Heading size={'3xl'} className='text-white py-2'>LOGO</Heading>

        <Card size="" variant="filled" className="rounded-2xl items-center px-4 pt-2 pb-8 w-full gap-2">
          <Heading size="2xl" className="">
            Cadastro
          </Heading>

          <SignInGoogleButton />

          <View className='w-full flex flex-col gap-2 pt-4 pb-6'>
            <View className='flex flex-col w-full gap-1'>
              <Text className='text-white pb-1 font-bold'>E-mail</Text>
              <Input size='xl' isInvalid={!emailValido}>
                <InputField
                  autoCapitalize="none"
                  value={emailAddress}
                  placeholder="seuemail@email.com"
                  onChangeText={(email) => setEmailAddress(email)}
                  type='text'
                  onBlur={() => { checkEmail(emailAddress) }}
                  autoComplete='email'
                />
              </Input>

              <Text className={`text-red-300 ${emailValido ? 'invisible' : ''}`}>E-mail inválido</Text>

            </View>

            <View className='flex flex-col w-full gap-1'>
              <Text className='text-white pb-1 font-bold'>Senha</Text>

              <Input size='xl' isInvalid={!senhaValida}>
                <InputField

                  value={password}
                  secureTextEntry={true}
                  onChangeText={(password) => checkSenha(password)}
                  type={mostrarSenha ? 'text' : 'password'}
                  onSubmitEditing={onSignUpPress}
                  autoCapitalize='none'
                  autoComplete='password'
                  placeholder='No mímimo 8 caracteres' />

                <InputSlot className="pr-4" onPress={handleState}>
                  <InputIcon as={mostrarSenha ? EyeIcon : EyeOffIcon} />
                </InputSlot>
              </Input>

              <Text className={`text-red-300 ${senhaValida ? 'invisible' : ''}`}>Senha inválida</Text>

            </View>
          </View>

          <Button onPress={onSignUpPress} variant='solid' action='primary' size='xl' className='w-full transition disabled:bg-primary-black'>
            <ButtonSpinner className={loading ? 'data-[active=true]:text-neutral-100' : 'hidden'} color='white'></ButtonSpinner>
            <ButtonText className='text-white font-bold pl-4 data-[disabled=true]:text-neutral-500'>Continuar</ButtonText>
          </Button>

          <View className='flex-row pt-4'>
            <Link href="/(auth)/trocar-senha" className='text-primary-light underline'>
              Esqueci minha senha
            </Link>
          </View>
        </Card>

        <View className='flex-row'>
          <Text className='text-white'>Já possui uma conta?</Text>

          <Link href="/(auth)/login">
            <Text className='text-primary-light'>Entrar</Text>
          </Link>
        </View>

      </Pressable>

    </SafeAreaView>
    </>
  )
}