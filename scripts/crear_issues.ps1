# Crea las etiquetas y las issues del backlog en tu repositorio de GitHub.
# Requisitos: GitHub CLI instalado (https://cli.github.com) y sesión iniciada con: gh auth login
# Uso (desde la carpeta del proyecto):  .\scripts\crear_issues.ps1

$etiquetas = @{
  "diseno"  = "1D76DB"; "entorno" = "5319E7"; "bloque-1" = "0B3987";
  "bloque-2" = "3A6FC4"; "bloque-3" = "E0A526"; "entrega" = "C62828"; "cierre" = "666666"
}
foreach ($e in $etiquetas.Keys) { gh label create $e --color $etiquetas[$e] --force | Out-Null }

$mapa = @{
  "## Diseño" = "diseno"; "## Entorno" = "entorno"; "## Bloque 1" = "bloque-1";
  "## Entrega 1" = "entrega"; "## Bloque 2" = "bloque-2"; "## Bloque 3" = "bloque-3"; "## Cierre" = "cierre"
}

$etiqueta = $null
Get-Content "docs/backlog.md" -Encoding UTF8 | ForEach-Object {
  $linea = $_
  foreach ($k in $mapa.Keys) { if ($linea.StartsWith($k)) { $etiqueta = $mapa[$k] } }
  if ($linea -match '^- \[ \] (.+)$' -and $etiqueta) {
    $titulo = $Matches[1]
    gh issue create --title $titulo --body "Tarea del backlog del proyecto." --label $etiqueta | Out-Null
    Write-Host "Creada: [$etiqueta] $titulo"
  }
}
Write-Host "Listo. Añade las issues a tu GitHub Project desde la pestaña Projects."
