@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ========== 1) Default values and constants ==========
set "API=claude"
set "FOLDER_PREFIX=TEST-single-REGEN-BS"

:: Hyperparameters
set "MAX_CODE_TOKEN_LENGTH=20000"
set "MAX_FIX_BUG_TRIES=10"
set "MAX_REGENERATE_TRIES=10"
set "MAX_FEEDBACK_GEN_CODE_TRIES=5"
set "MAX_MLLM_FIX_BUGS_TRIES=5"
set "FEEDBACK_ROUNDS=2"

:: ========== 用户个性化配置 ==========
:: 要生成的知识点 (修改此处)
set "KNOWLEDGE_POINT=二分搜索"

:: ========== 2) Execute ==========
echo ==========================================
echo    Code2Video - 知识点视频生成
echo ==========================================
echo 知识点: %KNOWLEDGE_POINT%
echo API: %API%
echo ==========================================

:: 用户画像描述 user_profile

python agent.py ^
  --API "%API%" ^
  --folder_prefix "%FOLDER_PREFIX%" ^
  --use_feedback ^
  --use_assets ^
  --max_code_token_length "%MAX_CODE_TOKEN_LENGTH%" ^
  --max_fix_bug_tries "%MAX_FIX_BUG_TRIES%" ^
  --max_regenerate_tries "%MAX_REGENERATE_TRIES%" ^
  --max_feedback_gen_code_tries "%MAX_FEEDBACK_GEN_CODE_TRIES%" ^
  --max_mllm_fix_bugs_tries "%MAX_MLLM_FIX_BUGS_TRIES%" ^
  --feedback_rounds "%FEEDBACK_ROUNDS%" ^
  --knowledge_point "%KNOWLEDGE_POINT%" ^
  --user_profile "我是17岁的高中生,想要的学习难度是入门级,选择的编程语言是Python,目标是利用暑假成功入门Python,完成一个自己的小项目,目前已有的知识储备是Python的输入输出语法和最基础的函数的语法"

pause
