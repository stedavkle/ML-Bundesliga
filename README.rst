Teamproject Sportvorhersage |Bundesliga-Logo|
-----------
.. |Bundesliga-Logo| image:: web\img\bl.png
    :width: 400
    :alt: Bundesliga-Logo

space for badges
# license badge

What is our project about?
======
We started this project to predict the results of games of the German Football Bundesliga.
It started as that, but as this project is programmed modal it is possible to be used for
any sport or league. You can see a glimpse of that, when you look at our implementation of the
Basketball League NBA.

But to be more precise, we wanted to use the data from past years and find
clever algorithms and use machine learning models to predict game results as accurate as possible.

We also wanted to enable a great user experience, that's why we were striving to make it very
easy for the user to set all the possible variables themselves. You can now decide which teams you want to predict,
which algorithm you want to use, with which data the models are trained and so on.

We'll then give you probabilities of a home win, a draw and a guest win.
With some models you can even get a prediction which exact score is most likely to be the end result.

There is a lot more to see, so let's get started.

Visuals
======
As we said, this project is about predicting sport games. But also to figure out, if there
are any interesting facts within the data. How often do draws happen and do our prediction algorithms
do a good job of finding them. Or is there a correlation between how many or little goals a team scores,
and their likeliness of winning? There are many interesting questions to be asked. But we decided to include these two.

First, to see the analyses of the draw frequency.

.. :image:: analyse.png
    :width: 400
    :alt:
(Count, how many draws there were over the last 3 seasons)

.. :image:: analyse.png
    :width: 400
    :alt: todo
(Count, how many draws we predicted with each algorithm over the last 3 seasons)


Installation
======
Bla, wie erstellt man das richtige Environment.

Once you've activated the environment, install the current package and its
dependencies with::

    cd ML-Bundesliga
    pip install -e .

Usage
======
After the package and all dependencies are installed,
you can execute the code that's contained in the teamproject/__main__.py by typing::

    python -m teamproject

If you have executed the pip install line above, you can also type for short::

    teamproject

Special Advantages
======
**What was our focus while developing?**

Our project stands out in terms of the user experience. We realised our user interface with **eel**, which is
a python library that allows you to create offline user interfaces, that are structured like websites.
Because we chose this implementation the project is cross-system, which then allows a big clientele.

We also focussed on robustness and accessibility. Therefore it is possible to jump to any of the previous steps
of the program, and if you accidentally or intentionally refresh the page, you will still be in the same spot in the process.
Furthermore, we added alternative texts to all the images, the UI is completely usable
with the keyboard and we also paid attention to design it very comprehensible.

Outside of the User Interface, we focussed on the modularity of the crawler and the models file. This means,
that any new algorithm can easily be implemented and will automatically be included in the GUI. We realised this
with abstract classes. It is also possible to create a new instance of the crawler, that means you can get
quickly implement different sports or international leagues.

**Which Algorithms did we use?**

We implemented four different algorithms. The first one is a very simple algorithm, we called it **MostWins**.
As the name implies, it analyses the selected games and sums the amount of times both teams won and drew.
Afterwards these sums are compared and the probabilities are returned accordingly.

The second one uses the **Poisson Model**. It calculates how likely it is for each team to make a certain amount of goals.
This calculation leaves a table where the rows represent the amount of goals team 1 is going to make. And the columns for team 2.
Therefore the diagonal of this calculation shows a draw.

The third model is the **Dixon-Coles Model**. Was genau ist das?

And the last model is the **Logistic Regression Model**. It calculates the outcome with logistic regression.
To do that, is generates factors for each team for a home win and a guest win. These
factors are compared, and calculates the probability of which outcome.

Tests
======
We focussed on testing everything thoroughly. To execute the tests, go on like this::

    python -m pytest tests/test_crawler.py
    python -m pytest tests/test_models.py

Roadmap
======

Project Status
======
active

Authors and Acknowledgement
======
The authors are Stephan Amann, Cornelius Bopp, David Kleindiek and Amelie Schäfer.
This project started as an university assignment, therefore we acknowledge and thank our tutors
Felix Dangel, Thomas Gläßle and Frank Schneider for their feedback and generous help.

License
======
This project is licensed under the permissive open source MIT license.