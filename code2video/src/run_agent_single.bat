@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ========== 1) Default values and constants ==========
set "API=claude"
set "FOLDER_PREFIX=TEST-single-REGEN-BS"

:: Hyperparameters
set "MAX_CODE_TOKEN_LENGTH=10000"
set "MAX_FIX_BUG_TRIES=10"
set "MAX_REGENERATE_TRIES=10"
set "MAX_FEEDBACK_GEN_CODE_TRIES=5"
set "MAX_MLLM_FIX_BUGS_TRIES=5"
set "FEEDBACK_ROUNDS=2"

:: ========== 用户个性化配置 ==========
:: 要生成的知识点 (修改此处)
set "KNOWLEDGE_POINT=二分搜索"

:: 目标受众年龄段: high_school(初高中生), college(大学/研究生), professional(职场人士)
set "AGE_GROUP=high_school"

:: 编程语言: Python, C, Java, C++, JavaScript, Go, Rust, C#, 伪代码
set "PROGRAMMING_LANGUAGE=C"

:: 难度级别: low(入门级), medium(进阶级), high(专家级)
set "DIFFICULTY=low"

:: ========== 2) Execute ==========
echo ==========================================
echo    Code2Video - 知识点视频生成
echo ==========================================
echo 知识点: %KNOWLEDGE_POINT%
echo 年龄段: %AGE_GROUP%
echo 编程语言: %PROGRAMMING_LANGUAGE%
echo 难度: %DIFFICULTY%
echo API: %API%
echo ==========================================

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
  --age_group "%AGE_GROUP%" ^
  --programming_language "%PROGRAMMING_LANGUAGE%" ^
  --difficulty "%DIFFICULTY%" ^
  --knowledge_point "%KNOWLEDGE_POINT%"

pause
