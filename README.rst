|run on repl.it|_

.. |run on repl.it| image:: https://repl.it/badge/github/myrmica-habilis/SzT
.. _run on repl.it: https://szt.myrmica.repl.run/

=============
Strach ze tmy
=============

Česká textová dobrodružná hra, původně vycházející ze `vzorové hry <https://github.com/myrmica-habilis/cave-terror>`__ vytvořené podle knihy `Make Your Own Python Text Adventure <https://www.apress.com/gp/book/9781484232309>`__. Postupně upravována, rozšiřována a přeložena do češtiny.

Spuštění
========

Hra vyžaduje Python 3.6 nebo vyšší. Doporučuji nejdříve vytvořit virtuální prostředí příkazem ``python3 -m venv .env`` v hlavní složce projektu (tedy tam, kde je i tento soubor README). Ze stejného místa pak spusťte hru příkazem ``.env/bin/python -m szt`` (resp. ve Windows příkazem ``.env\Scripts\python -m szt``).

Pokud virtuální prostředí nechcete, spustíte hru příkazem ``python3 -m szt``

Základní informace
==================

Automatické mapování
--------------------

Po příchodu na první křižovatku (tedy záhy po započetí hry) si vaše postava začne sama kreslit mapu, kterou si můžete kdykoliv zobrazit příkazem ``M``.

Režim rychlé chůze
------------------
Po lokacích, které jste už navštívili, se můžete pohybovat na libovolnou vzdálenost zrychleně. Jestliže např. vaše mapa vypadá takto:

.. code-block::

         ?
       ++H
       +
    ?+ ++
     +++
       +
       +
       +

a vy se chcete vydat na neprozkoumané místo na západě, přemístíte se tam jediným příkazem ``zzjjjzzsz``. (poznámka: pokud po cestě narazíte na živého nepřítele, režim zrychleného přesunu se přeruší a nepřítel na vás normálně zaútočí)

Útěk z boje
-----------

U většiny nepřátel se v průběhu boje může stát, že je nepřítel omráčen a na jedno kolo vyřazen z boje. V takové situaci je možné z lokace odejít. Tuto možnost je vhodné využít vždy, protože i když tudy budete ještě potřebovat projít, příště vám tentýž nepřítel pravděpodobně způsobí menší škodu (budete mít vyšší zkušenost a možná i lepší zbraň).

Ukázky
======

.. image:: screenshots/screenshot_console.png

.. image:: screenshots/screenshot_console_windows.png

.. image:: screenshots/screenshot_pycharm.png

.. image:: screenshots/screenshot_replit.png
