import discord
import os
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
    async def save(self, ctx, url: str) -> None:
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
