@echo off
cls

:: Delete existing failed stack
echo [1/4] Deleting old stack...
aws cloudformation delete-stack --stack-name genai-aws-multiagent-threatpulse
aws cloudformation wait stack-delete-complete --stack-name genai-aws-multiagent-threatpulse

:: Clear local SAM cache
echo [2/4] Cleaning cache...
if exist .aws-sam rd /s /q .aws-sam

:: Build application & check for errors
echo [3/4] Building...
call sam build
if %errorlevel% neq 0 (echo Build failed. & pause & exit /b %errorlevel%)

:: Deploy to AWS CloudFormation
echo [4/4] Deploying...
call sam deploy
