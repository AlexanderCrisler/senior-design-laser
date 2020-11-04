Imports Phidget22
Imports System
Imports System.Data
Imports System.Threading
Imports System.Globalization
Imports System.Speech.Synthesis
Imports System.Speech.Recognition

Class MainWindow

    Private Structure Equipment
        Public Name As String
        Public Location As Integer()
    End Structure

    'Public Event SpeechRecognitionRejected As EventHandler(Of SpeechRecognitionRejectedEventArgs)
    Dim SearchItems As New List(Of Equipment)
    Dim wordlist As String() = New String() {}
    Dim cult As New CultureInfo("en-US")
    Dim sre As New SpeechRecognitionEngine(cult)
    Dim synth As New SpeechSynthesizer

    Dim Axis1 As RCServo
    Dim Axis2 As RCServo

    Dim KeyboardThread As New Thread(AddressOf Moveup)


#Region "UI Stuff"
    Private Sub closedown() Handles Me.Closing
        Axis1.Close()
        Axis2.Close()
        sre.RecognizeAsyncStop()
        Dim FW As New IO.StreamWriter("items.txt", False)
        SearchItems(0) = New Equipment With {.Name = "Home", .Location = {0, 0}}
        For Each itm As Equipment In SearchItems
            FW.WriteLine(itm.Name & "+" & itm.Location(0) & "+" & itm.Location(1))
        Next
        FW.Close()
        KeyboardThread.Abort()
    End Sub

    Private Sub Dragging() Handles grdControls.MouseDown
        If Application.Current.MainWindow.WindowState = WindowState.Maximized Then Application.Current.MainWindow.WindowState = WindowState.Normal
        Application.Current.MainWindow.DragMove()
    End Sub

    Private Sub WinClose() Handles btnClose.Click

        Close()

    End Sub

    Private Sub WinMinimize() Handles btnMinimize.Click
        Me.WindowState = WindowState.Minimized
    End Sub

    Private Sub WinMaximize() Handles btnRestore.Click
        If Me.WindowState = WindowState.Maximized Then
            Me.WindowState = WindowState.Normal
        Else
            Me.WindowState = WindowState.Maximized
        End If
    End Sub

    Private Sub Themes() Handles cmbTheme.SelectionChanged

        Select Case cmbTheme.SelectedIndex
            Case 0
                My.Application.Resources.MergedDictionaries(0).Source = New Uri($"/Themes/Default.xaml", UriKind.Relative)
            Case 1
                My.Application.Resources.MergedDictionaries(0).Source = New Uri($"/Themes/ExpressionDark.xaml", UriKind.Relative)
            Case 2
                My.Application.Resources.MergedDictionaries(0).Source = New Uri($"/Themes/ExpressionLight.xaml", UriKind.Relative)
            Case 3
                My.Application.Resources.MergedDictionaries(0).Source = New Uri($"/Themes/ShinyBlue.xaml", UriKind.Relative)
            Case 4
                My.Application.Resources.MergedDictionaries(0).Source = New Uri($"/Themes/ShinyRed.xaml", UriKind.Relative)
        End Select
    End Sub


    Private Sub SearchFunction() Handles btnSearch.Click, txbSearch.KeyDown
        For Each item As ListBoxItem In lbxitems.Items
            If txbSearch.Text = "" OrElse Not item.Content.ToString().ToLower.Contains(txbSearch.Text.ToLower) Then
                item.Visibility = Visibility.Collapsed
            Else
                item.Visibility = Visibility.Visible
            End If
        Next
    End Sub


    Private Sub PointLaser() Handles lbxitems.SelectionChanged
        Dim tempthread As New Thread(
            Sub()
                Axis1.Engaged = True
                Axis2.Engaged = True
                Dispatcher.Invoke(
                Sub()
                    Axis1.TargetPosition = SearchItems(lbxitems.SelectedIndex).Location(0)
                    Axis2.TargetPosition = SearchItems(lbxitems.SelectedIndex).Location(1)
                End Sub)
            End Sub)
        tempthread.Start()
    End Sub

    Private Sub btnAdd_Click() Handles btnAdd.Click

        Dim Tempeqip As New Equipment With {.Name = txbName.Text, .Location = {Axis1.Position, Axis2.Position}}
        Dim tempitem As New ListBoxItem
        tempitem.Content = txbName.Text
        SearchItems.Add(Tempeqip)
        lbxitems.Items.Add(tempitem)
    End Sub


    Private Sub Startupstuff() Handles Me.Loaded

        SearchItems.Add(New Equipment With {.Name = "Home", .Location = {0, 0}})

        If My.Computer.FileSystem.FileExists("items.txt") Then
            Dim FR As New IO.StreamReader("items.txt")
            FR.ReadLine()
            Do While FR.Peek > -1
                Dim Tempstring As String = FR.ReadLine()
                Dim TempArray As String() = Tempstring.Split("+")
                Dim tempequip As Equipment
                tempequip.Name = TempArray(0)
                tempequip.Location = {TempArray(1), TempArray(2)}
                SearchItems.Add(tempequip)
            Loop
            FR.Close()
        End If

        For Each item As Equipment In SearchItems
            Dim newitem As New ListBoxItem
            newitem.Content = item.Name
            lbxitems.Items.Add(newitem)
        Next

        MotorSetup()
        VoiceSetup()
        KeyboardThread.Start()
    End Sub
#End Region



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
            MessageBox.Show(ex.Message)
            Me.Close()
            Exit Sub
        End Try

        Axis1.MinPulseWidth = 600
        Axis1.MaxPulseWidth = 2300
        Axis2.MinPulseWidth = 600
        Axis2.MaxPulseWidth = 2300

        Axis1.VelocityLimit = 500
        Axis2.VelocityLimit = 500
        Axis1.Acceleration = 200
        Axis2.Acceleration = 200

        Axis1.TargetPosition = 0
        Axis2.TargetPosition = 0
        Axis1.Engaged = True
        Axis2.Engaged = True
        Thread.Sleep(1000)
        Axis1.Engaged = False
        Axis2.Engaged = False


    End Sub

    Private Sub VoiceSetup()


        synth.SetOutputToDefaultAudioDevice()
        synth.SelectVoiceByHints(VoiceGender.Female, VoiceAge.Teen)
        synth.Rate = 2
        'synth.Speak("Hello, my name is Alis. How may I help you today?")



        sre.SetInputToDefaultAudioDevice()
        AddHandler sre.SpeechRecognized, AddressOf sre_SpeechRecognized
        'Dim Diction As System.Speech.Recognition.DictationGrammar = New System.Speech.Recognition.DictationGrammar
        Dim Directions As Choices = New Choices()
        For Each item As ListBoxItem In lbxitems.Items
            Directions.Add(item.Content)
        Next
        Dim MyGram As New Grammar(New GrammarBuilder(Directions))
        sre.LoadGrammar(MyGram)
        sre.RecognizeAsync(RecognizeMode.Multiple)
    End Sub



    Private Sub sre_SpeechRecognized(sender As Object, e As SpeechRecognizedEventArgs)
        Dim txt As String = e.Result.Text
        Dim conf As Single = e.Result.Confidence
        Dim temp As ItemCollection = lbxitems.Items
        If conf < 0.8 Then Return
        For Each item As ListBoxItem In lbxitems.Items
            If item.Content = txt Then
                lbxitems.SelectedItem = item
                Exit For
            End If
        Next
    End Sub

    Private Sub Moveup()

        Dim count As Integer = 0
        Dim tempval As Integer
        Dim increment As Double
        While True
            Dispatcher.Invoke(
                Sub()
                    If Keyboard.IsKeyDown(Key.Up) Then
                        tempval = 1
                    ElseIf Keyboard.IsKeyDown(Key.Down) Then
                        tempval = 2
                    ElseIf Keyboard.IsKeyDown(Key.Right) Then
                        tempval = 3
                    ElseIf Keyboard.IsKeyDown(Key.Left) Then
                        tempval = 4
                    Else
                        tempval = 0
                    End If
                End Sub)


            Select Case tempval
                Case 1
                    count += 1
                    If Not Axis2.Engaged Then Axis2.Engaged = True
                    If Axis2.TargetPosition + increment < 180 Then Axis2.TargetPosition += increment
                Case 2
                    count += 1
                    If Not Axis2.Engaged Then Axis2.Engaged = True
                    If Axis2.TargetPosition - increment > 0 Then Axis2.TargetPosition -= increment
                    increment += 1
                Case 3
                    count += 1
                    If Not Axis1.Engaged Then Axis1.Engaged = True
                    If Axis1.TargetPosition + increment < 180 Then Axis1.TargetPosition += increment
                    increment += 1
                Case 4
                    count += 1
                    If Not Axis1.Engaged Then Axis1.Engaged = True
                    If Axis1.TargetPosition - increment > 0 Then Axis1.TargetPosition -= increment
                    increment += 1
                Case Else
                    increment = 0.1
            End Select
            If count > 10 Then increment += 1
            Thread.Sleep(100)

        End While
    End Sub


End Class
