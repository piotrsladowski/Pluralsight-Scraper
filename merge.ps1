$num1 = read-host -Prompt "Enter Ist number"
$num2 = Read-Host -Prompt "Enter Second number - inclusive" 

[int]$Num1 = [convert]::ToInt32($num1, 10)
[int]$Num2 = [convert]::ToInt32($num2, 10)

$dirname="merged"
$path = "$PSScriptRoot\$dirname"
If(!(test-path $path))
{
      New-Item -ItemType Directory -Force -Path $path
}

for($i = $num1; $i -le $num2; $i++)
{
    $video= Get-ChildItem ("video_{0}_*.ts" -f $i) | Select-Object -Expand Name
    $audio= Get-ChildItem ("audio_{0}_*.aac" -f $i) | Select-Object -Expand Name
    $output="$i.mp4"
    iex ".\ffmpeg.exe -i .\$video -i .\$audio -c:v copy -c:a copy .\$dirname\$output"
}