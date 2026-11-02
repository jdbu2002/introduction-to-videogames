ONDA ESTELAR - Ejercicio 04 (MISW-4407 Desarrollo de Videojuegos)
=================================================================

Enlace en itch.io:
    https://<usuario>.itch.io/<proyecto>

Controles
---------
- Flechas: mover la nave
- Click izquierdo: disparar hacia el cursor
- Espacio o click derecho: ONDA DE CHOQUE (especial)
- P: pausar / reanudar

Caracteristica unica: Onda de choque
------------------------------------
Al activarla, la nave libera una onda expansiva circular que destruye a todos
los enemigos que alcanza. Despues de usarla debe recargarse durante 4 segundos.
- La recarga se ve en la barra inferior izquierda y en un contador "ONDA 3.2s".
- Cuando esta lista, la barra pulsa, destella y suena un aviso ("LISTA!").
- Si se intenta usar sin carga, la barra parpadea en rojo con un sonido de error.
- Game feel: sacudida de camara, onda con easing que se desvanece, explosiones.
Configuracion en assets/cfg/special.json y textos/HUD en assets/cfg/interface.json.

Ejecucion local
---------------
    uv run python exercise-4/main.py

Build web (itch.io, tipo HTML)
------------------------------
    uv run pygbag --build --ume_block 0 exercise-4
    Subir un zip con el contenido de exercise-4/build/web (index.html,
    exercise-4.apk, favicon.png) y marcar "This file will be played in the browser".

Creditos
--------
- Sprites, fuente y sonidos base: recursos del curso MISW-4407.
- Sonidos shockwave/ready/denied/move: generados proceduralmente para este proyecto.
- esper 2.5 (MIT) incluido en exercise-4/esper para la version web.
