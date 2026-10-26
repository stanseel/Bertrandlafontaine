# Bertrand Lafontaine

Website voor Bertrand Lafontaine: documentaires, teksten en gesprekken over kunst, vormgeving en architectuur.

Online: https://stanseel.github.io/Bertrandlafontaine/

## Opbouw

- `_bron/inhoud.json`: films, filmografie en tekstprojecten (uit masterdocument v05).
- `_bron/build.py`: maakt alle pagina's. Vaste teksten (home, over, gesprek, nieuws) staan bovenaan dit script.
- `assets/`: stijl, script, verkleinde beelden en de twee homepage-loops.
- `styleguide.html`: stijlgids.
- `Input/`: bronmateriaal (Word, stills, video). Staat niet in git.

## Bouwen

```bash
python3 _bron/build.py
```

Beelden worden enkel opnieuw gemaakt als ze nog niet in `assets/beeld/` staan. Verwijder een bestand daar om het opnieuw te laten maken.
