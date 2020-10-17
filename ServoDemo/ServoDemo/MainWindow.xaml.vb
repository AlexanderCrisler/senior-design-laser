Imports Phidget22
Imports System
Imports System.Data
Imports System.Threading
Imports System.Globalization
Imports System.Speech.Synthesis
Imports System.Speech.Recognition

Class MainWindow


    'Public Event SpeechRecognitionRejected As EventHandler(Of SpeechRecognitionRejectedEventArgs)

    Dim wordlist As String() = New String() {"alis", "Up", "Down", "Left", "Right", "Home", "0"}
    Dim cult As New CultureInfo("en-US")
    Dim sre As New SpeechRecognitionEngine(cult)
    Dim synth As New SpeechSynthesizer

    Dim Axis1 As RCServo
    Dim Axis2 As RCServo


    Private Sub MotorSetup()
        Try
            Axis1 = New RCServo()
            Axis2 = New RCServo()
            Axis1.Channel = 0
            Axis2.Channel = 1
            Axis1.Open(5000)
            Axis2.Open(5000)
        Catch ex As Exception
            MessageBox.Show("Could not connect to phiget")
            Me.Close()
        End Try

        Axis1.VelocityLimit = 3000
        Axis2.VelocityLimit = 3000
        Axis1.Acceleration = 3000
        Axis2.Acceleration = 3000

        Axis1.TargetPosition = 90
        Axis2.TargetPosition = 90
        Axis1.Engaged = True
        Axis2.Engaged = True
    End Sub

    Private Sub VoiceSetup()


        synth.SetOutputToDefaultAudioDevice()
        synth.SelectVoiceByHints(VoiceGender.Female, VoiceAge.Teen)
        synth.Rate = 2
        synth.Speak("Hello, my name is Alis. How may I help you today?")



        sre.SetInputToDefaultAudioDevice()
        AddHandler sre.SpeechRecognized, AddressOf sre_SpeechRecognized
        'Dim Diction As System.Speech.Recognition.DictationGrammar = New System.Speech.Recognition.DictationGrammar
        Dim Directions As Choices = New Choices()
        Directions.Add(wordlist)
        Dim MyGram As New Grammar(New GrammarBuilder(Directions))
        sre.LoadGrammar(MyGram)
        sre.RecognizeAsync(RecognizeMode.Multiple)
    End Sub

    Private Sub Startupstuff() Handles Me.Loaded
        MotorSetup()
        VoiceSetup()

    End Sub

    Private Sub sre_SpeechRecognized(sender As Object, e As SpeechRecognizedEventArgs)
        Dim txt As String = e.Result.Text
        Dim conf As Single = e.Result.Confidence
        If conf < 0.65 Then Return

        If txt.ToLower().Contains("up") Then
            If Axis2.TargetPosition >= 170 Then
                synth.Speak("I am sorry, that is outside of my range")
                Return
            End If
            Axis2.TargetPosition = Axis2.Position + 5

        ElseIf txt.ToLower().Contains("down") Then
            If Axis2.TargetPosition <= 10 Then
                synth.Speak("I am sorry, that is outside of my range")
                Return
            End If
            Axis2.TargetPosition = Axis2.Position - 5
        ElseIf txt.ToLower().Contains("left") Then
            If Axis1.TargetPosition >= 170 Then
                synth.Speak("I am sorry, that is outside of my range")
                Return
            End If
            Axis1.TargetPosition = Axis1.Position + 5
        ElseIf txt.ToLower().Contains("right") Then
            If Axis1.TargetPosition <= 10 Then
                synth.Speak("I am sorry, that is outside of my range")
                Return
            End If
            Axis1.TargetPosition = Axis1.Position - 5
        ElseIf txt.ToLower().Contains("home") Then
            Axis1.TargetPosition = 90
            Axis2.TargetPosition = 90
        ElseIf txt.ToLower().Contains("0") Then
            Axis1.TargetPosition = 0
            Axis2.TargetPosition = 0
        End If
    End Sub

    Private Sub closedown() Handles Me.Closing
        Axis1.Close()
        Axis2.Close()


    End Sub

End Class
