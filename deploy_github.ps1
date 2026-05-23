# ============================================================
# DEPLOY A GITHUB PAGES - Script para PowerShell
# ============================================================
# Tu usuario de GitHub: eliecerzunigab-gif
# Repositorio: central-ovnis-dashboard
# ============================================================

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🚀 SUBIENDO DASHBOARD A GITHUB PAGES" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# 1. Primero regenerar los datos más recientes
Write-Host "`n📊 Regenerando datos desde gov/war/ufo..." -ForegroundColor Yellow
python generate_dashboard_v3.py
python translate_data.py
python rebuild_dashboard.py

# 2. Inicializar git (si no existe)
if (-not (Test-Path ".git")) {
    Write-Host "`n📦 Inicializando repositorio git..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# 3. Crear .gitignore
@"
__pycache__/
*.pyc
*.pyo
.DS_Store
*.csv
explore_*.py
aaro_script.txt
war_ufo_*.html
"@ | Out-File -FilePath ".gitignore" -Encoding utf8

# 4. Agregar archivos importantes
Write-Host "`n📄 Agregando archivos al repositorio..." -ForegroundColor Yellow
git add dashboard_ufo.html
git add dashboard_data.json
git add slideshow_images.json
git add .gitignore
git add generate_dashboard_v3.py
git add generate_dashboard_final.py
git add translate_data.py
git add rebuild_dashboard.py
git add extract_slideshow.py
git add parse_war_ufo.py
git add README.md

# 5. Commit
Write-Host "`n💾 Haciendo commit..." -ForegroundColor Yellow
git commit -m "Dashboard UFO - datos combinados desde gov/war/ufo ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"

# 6. Configurar remote
$remoteUrl = "https://github.com/eliecerzunigab-gif/central-ovnis-dashboard.git"
$remotes = git remote
if (-not ($remotes -contains "origin")) {
    Write-Host "`n🔗 Configurando remote origin..." -ForegroundColor Yellow
    git remote add origin $remoteUrl
} else {
    Write-Host "`n🔗 Actualizando remote origin..." -ForegroundColor Yellow
    git remote set-url origin $remoteUrl
}

# 7. Subir a GitHub
Write-Host "`n☁️ Subiendo a GitHub..." -ForegroundColor Yellow
Write-Host "   Repositorio: $remoteUrl" -ForegroundColor Gray
Write-Host "`n⚠️  IMPORTANTE: Te pedirá usuario y contraseña (o token personal)" -ForegroundColor Magenta
Write-Host "   Si usas autenticación de dos factores, necesitas un token:" -ForegroundColor Magenta
Write-Host "   GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)" -ForegroundColor Magenta
Write-Host "   Crea uno con permisos 'repo' y úsalo como contraseña.`n" -ForegroundColor Magenta

git push -u origin main

# 8. Instrucciones finales
Write-Host "`n==================================" -ForegroundColor Green
Write-Host "✅ SUBIDA COMPLETADA!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host "`n📌 Ahora activa GitHub Pages:" -ForegroundColor Cyan
Write-Host "   1. Ve a: https://github.com/eliecerzunigab-gif/central-ovnis-dashboard" -ForegroundColor White
Write-Host "   2. Settings → Pages" -ForegroundColor White
Write-Host "   3. Source: 'Deploy from a branch'" -ForegroundColor White
Write-Host "   4. Branch: 'main' / '(root)'" -ForegroundColor White
Write-Host "   5. Save" -ForegroundColor White
Write-Host "`n🌐 Tu dashboard estará en:" -ForegroundColor Cyan
Write-Host "   https://eliecerzunigab-gif.github.io/central-ovnis-dashboard/dashboard_ufo.html" -ForegroundColor Green
Write-Host "`n⏱️  Espera 1-2 minutos después de activar Pages." -ForegroundColor Yellow
