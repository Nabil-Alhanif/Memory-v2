import discord
import os
import random
import re
import requests

from bs4 import BeautifulSoup
from discord.ext import commands
from time import time

import cogs.scraper.utilities as util

class PageData:
    def __init__(self, author, url) -> None:
        self.author = author
        self.url = url

    def scrape(self) -> None:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        self.title = str(soup.find("title"))

        subject = re.findall(r'>(.*?) [|]', self.title)
        self.subject = " | ".join(subject)

        diff = re.findall(r'[(](.*?)[)]', self.title)
        self.diff = " | ".join(diff)

        cur_time = str(time())

        self.name = self.subject + " - " + self.diff
        self.question_file = str(self.author) + " - Questions - " + cur_time + " - " + self.name
        self.solution_file = str(self.author) + " - Solutions - " + cur_time + " - " + self.name

        questions = soup.find_all("div", class_="question-problem")
        self.questions = util.extractImgFromHtml(questions)

        solutions = soup.find_all("script")
        self.solutions = util.extractImgFromHtml(solutions)

class SaveMyExams(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="dsme", help="Extract a question topic from savemyexams.co.uk with specific difficulties into a pdf file")
    async def dsme(self, ctx, url: str) -> None:
        # Validate the url
        if not util.uriValidate(url):
            await ctx.send(f'Hey {ctx.author.mention}, the url you send is not valid! Please check it again!')
            return

        # Validate that the link is really of savemyexams.co.uk
        if not url.startswith("https://www.savemyexams.co.uk"):
            await ctx.send(f'Hey {ctx.author.mention}, the link you send is not one of savemyexams.co.uk! Please check it again!')

        await ctx.send(f'Hey {ctx.author.mention}, I\'m processing your request! This process will usually take less than 1 minute depending on the amount of requests I\'m currently processing!')

        # Scrape the webpage
        data = PageData(ctx.author, url)
        data.scrape()

        util.extractImgToPdf(data.questions, data.question_file)
        util.extractImgToPdf(data.solutions, data.solution_file)

        outputs = [
            discord.File(data.question_file + ".pdf", "Questions - " + data.name + ".pdf"),
            discord.File(data.solution_file + ".pdf", "Solutions - " + data.name + ".pdf"),
        ]

        await ctx.send(f'Hey {ctx.author.mention}, here are the files you requested!', files = outputs)

        # Cleanup
        os.remove(data.question_file + ".pdf")
        os.remove(data.solution_file + ".pdf")

    @commands.command(name="dsmes", help="Extract a question topic from savemyexams.co.uk")
    async def dsmes(self, ctx, url: str, easy_question_count: int = 5, medium_question_count: int = 3, hard_question_count: int = 2) -> None:
        # Validate the url
        if not util.uriValidate(url):
            await ctx.send(f'Hey {ctx.author.mention}, the url you send is not valid! Please check it again!')
            return

        # Validate that the link is really of savemyexams.co.uk
        if not url.startswith("https://www.savemyexams.co.uk"):
            await ctx.send(f'Hey {ctx.author.mention}, the link you send is not one of savemyexams.co.uk! Please check it again!')

        await ctx.send(f'Hey {ctx.author.mention}, I\'m processing your request! This process will usually take less than 1 minute depending on the amount of requests I\'m currently processing!')

        urls = util.processDifficulty(url)

        # Scrape the webpage
        easy_rawdata = PageData(ctx.author, urls["easy"])
        easy_rawdata.scrape()

        medium_rawdata = PageData(ctx.author, urls["medium"])
        medium_rawdata.scrape()

        hard_rawdata = PageData(ctx.author, urls["hard"])
        hard_rawdata.scrape()

        # Get important variable
        subject = str(easy_rawdata.subject)

        easy_data = []
        medium_data = []
        hard_data = []

        # We can use *.questions here,
        # as question and solutions should have the same amount
        for i in range(len(easy_rawdata.questions)):
            easy_data.append([easy_rawdata.questions[i], easy_rawdata.solutions[i]])

        for i in range(len(medium_rawdata.questions)):
            easy_data.append([medium_rawdata.questions[i], medium_rawdata.solutions[i]])

        for i in range(len(hard_rawdata.questions)):
            easy_data.append([hard_rawdata.questions[i], hard_rawdata.solutions[i]])

        # Make sure the question count is at most the same
        # as the amount of questions available
        easy_question_count = min(easy_question_count, len(easy_data))
        medium_question_count = min(medium_question_count, len(medium_data))
        hard_question_count = min(hard_question_count, len(hard_data))

        easy_selection = random.sample(easy_data, easy_question_count)
        medium_selection = random.sample(medium_data, medium_question_count)
        hard_selection = random.sample(hard_data, hard_question_count)

        questions = []
        solutions = []

        for i in [easy_selection, medium_selection, hard_selection]:
            for j in i:
                questions.append(j[0])
                solutions.append(j[1])

        cur_time = str(time())

        question_file = str(ctx.author) + " - Questions - " + cur_time + subject
        solution_file = str(ctx.author) + " - Solutions - " + cur_time + subject

        util.extractImgToPdf(questions, question_file)
        util.extractImgToPdf(solutions, solution_file)

        outputs = [
            discord.File(question_file + ".pdf", "Questions - " + subject + ".pdf"),
            discord.File(solution_file + ".pdf", "Solutions - " + subject + ".pdf"),
        ]

        await ctx.send(f'Hey {ctx.author.mention}, here are the files you requested!', files = outputs)

        # Cleanup
        os.remove(question_file + ".pdf")
        os.remove(solution_file + ".pdf")
