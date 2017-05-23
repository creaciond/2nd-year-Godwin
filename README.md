**NB (rus):** всё, что написано в этом readme, переведено на английский. Разделы, как правило, идут так: (раздел 1 по-русски), (раздел 1 по-английски), (раздел 2 по-русски), etc. Если вы вдруг увидите ошибку или опечатку, [напишите мне, пожалуйста](mailto:daria.maximova.m@gmail.com). Спасибо!

**NB (eng):** everything written in this readme is translated into English by myself. Parts are usually in the following order: (part 1, Russian), (part 1, English), (part 2, Russian) and so on. In case you noticed a typo or an error, please, do not hesitate to [write me about it](mailto:daria.maximova.m@gmail.com). Thanks in advance!

# Godwin's Law in vk.com
2nd year project, National Research University "Higher School of Economics", Moscow, Russia.

Курсовая второго курса, НИУ ВШЭ-Москва.

## Это интересно (на русском)
Похожая работа уже делалась для реддита, посмотреть можно [тут](http://www.zmescience.com/science/news-science/reddit-godwin-law/).

*Срок сдачи:* 29 мая 2017.

## Trivia (in English)
Something similar for reddit is [here](http://www.zmescience.com/science/news-science/reddit-godwin-law/).

*Work is due:* May 29, 2017.

## По-русски
**Что делает эта программа:** выкачивает посты из ВКонтакте, используя VK API, затем обрабатывает их, используя Томита-парсер и регулярные выражения, а затем проводит статистический анализ, вычисляя различные параметры, например, корреляцию.

**Как устроен репозиторий**

Основной и самый важный код — в корневой папке репозитория.

В папке ```data``` всё, что используется по ходу исследования — от исходых JSON-файлов до готовых ```.tsv```.

В папке ```tomita``` все файлы для Томита-парсера:
* грамматики,
* словари,
* газеттиры.

Папка ```results``` используется для складирования всех результатов и полученных графиков-визуализаций.
### Данные
Лежат на [гугл-диске](https://drive.google.com/open?id=0ByKwDDZBrG9HUDNVbTJUM0RpYjA) — файлы ```.tsv```, общий размер — около 300 Мб.

### Ход программы:

*1. Выкачивание постов*: файлы ```metadata-and-posts.py```, ```get_data_from_json.py```.

Некоторые посты были предоставлены в виде JSON-файлов следующего формата:
```
{
	"id_поста":
		[
			{
				"text": "текст поста",
			},
			[
				{
					"reply_to_uid": "id юзера, которому отвечают",
					"from_id": "id юзера, который пишет",
					"text": "текст комментария"
				},
			]
		]
}
```
Они же, в преобразованном виде, лежат в ```posts.tsv``` и ```comments.tsv```. То, что получилось в ходе работы (i.e. все данные исследования), лежит в папке ```data``` этого репозитория. ```metadata-and-posts.py``` генерирует файлы формата ```.tsv```, которые имеют имена типа ```(имя сообщества)_posts.tsv``` или ```(имя сообщества)_comments.tsv```.

*2. Обработка при помощи Томита-парсера:* файл ```analysis.py```. Файлы для Томита-парсера (словари, грамматики, etc.) лежат в папке ```tomita``` этого репозитория.

*3. Анализ полученных результатов*

To be soon

## In English
**What does this program do:** gets posts and comments from VKontakte via VK API, then parses them, using Tomita-parser and regular expressions; later on, it does some statistical analysis, calculating various parameters, such as correlation.

**What does this repo consist of**

The main and the most important code is in the repository root.

The ```data``` folder has all the data used throughout the research, both JSON files and ready ```.tsv``` files.

Folder called ```tomita``` includes all the files necessary for the Tomita parser, such as:
* grammars,
* lexicons,
* gazetteers.

The ```results``` folder is used for holding all the results of the research and visualization charts.

### How does it work

*1. Getting posts and comments*: files ```metadata-and-posts.py```, ```get_data_from_json.py```.

Some data was presented as JSON-files of the following structure:
```
{
	"post_id":
		[
			{
				"text": "text of a particular post",
			},
			[
				{
					"reply_to_uid": "id of a user whom a reply is addressed",
					"from_id": "id of a user writing",
					"text": "text of a particular comment"
				},
			]
		]
}
```
The same data is in ```posts.tsv``` and ```comments.tsv```. Other data of this research is in the ```data```folder of this repository. ```metadata-and-posts.py``` generates files of ```.tsv``` format, which have the names like ```(community domain)_posts.tsv``` или ```(community domain)_comments.tsv```.

*2. Parsing via Tomita parser:* code is in file ```analysis.py```. All the files for Tomita parser (such as grammars, etc.) are in the ```tomita``` folder of this repository.

*3. Analysis of the results*

To be soon
