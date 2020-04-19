|run on repl.it|_

.. |run on repl.it| image:: https://repl.it/badge/github/myrmica-habilis/SzT
.. _run on repl.it: https://szt.myrmica.repl.run/

=============
Strach ze tmy
=============

Česká textová dobrodružná hra, původně vycházející ze `vzorové hry <https://github.com/myrmica-habilis/cave-terror>`__ vytvořené podle knihy `Make Your Own Python Text Adventure <https://www.apress.com/gp/book/9781484232309>`__. Postupně upravována, rozšiřována a přeložena do češtiny.

Instalace a spuštění
====================

V libovolné složce, do níž máte oprávnění zapisovat, si naklonujte tento repozitář příkazem:

``git clone https://github.com/myrmica-habilis/SzT.git``

a přepněte se do hlavní složky projektu:

``cd SzT``

Hra vyžaduje instalaci jedné externí knihovny, proto doporučuji nejdříve vytvořit virtuální prostředí příkazem:

``python3 -m venv .env``

(poznámka: hra vyžaduje Python 3.6.1 nebo vyšší)

V nově vzniklém prostředí nejdříve aktualizujte správce balíčků:

``.env/bin/python -m pip install --upgrade pip setuptools``

a následně nainstalujte knihovnu `rich <https://rich.readthedocs.io>`__, kterou hra využívá k obarvení textů:

``.env/bin/python -m pip install rich``

Pak už můžete hru spustit příkazem:

``.env/bin/python -m szt``

Při spouštění z příkazové řádky je možné použít tyto parametry:

``-T`` pro nastavení tmavších barev

``-B`` pro režim obyčejného textu bez barev

``-R`` pro rychlý výpis textu bez efektu plynulého rolování

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

Většinu nepřátel ve hře lze v průběhu boje s trochou štěstí omráčit a na jedno kolo vyřadit z boje. V takové situaci je možné z lokace odejít.

Léčení
------

Léčivé prostředky vám navýší zdraví maximálně na úroveň 100 %, i když jejich léčivá síla je případně vyšší, než kolik vám do plného zdraví zbývá. Výjimkou je nejsilnější elixír, který má moc vám zvýšit zdraví i nad limit 100 %.

Ukázky
======

.. image:: screenshots/screenshot_console.png

.. image:: screenshots/screenshot_console_windows.png

.. image:: screenshots/screenshot_pycharm.png

.. image:: screenshots/screenshot_replit.png
