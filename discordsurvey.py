import discord
from discord.ext import commands
import sys
from os import path
import os
import string

#General Bot creation
bot=commands.Bot(command_prefix="!", description='records answers to pointless questions', command_not_found="That command doesn't exist. Try !help to see available commands.")

#Returns list of data from file based on input
def fetchResponses(Path):
	try:
		responseFile=open(Path,"r")
	except FileNotFoundError:
		return("Error")
	else:
		responseData=responseFile.read()
		responseData=responseData.split("\n")
		responseFile.close()
		return responseData

#Error Messages
number_error_message="`Use Question# instead of text. (Try !questions to see which question #`)"
permission_error_message="`You do not have permission to execute this command`"
file_not_found_message="`File not found when attempting to fetch data`"

#List of short answer questions and multiple choice questions
surveys=fetchResponses(r'C:\Users\User\Desktop\program crap\discordSurvey\surveys.txt')
surveys2=fetchResponses(r'C:\Users\User\Desktop\program crap\discordSurvey\surveys2.txt')
#Removing any extra empty lines
try:
	surveys.remove("")
except ValueError:
	pass
try:
	surveys2.remove("")
except ValueError:
	pass

print("logging in...\n")

#Log in check on console
@bot.event
async def on_ready():
	print("Logged in as")
	print(bot.user.name)	

#Quitting the program client side
@bot.command(help="quits the bot. Requires administration privelages. Use with caution, because getting the bot back online without access to the program itself is not reasonably possible",brief="close the bot",pass_context=True)
async def quit(ctx):
	if 'utopians' in (y.name.lower() for y in ctx.message.author.roles):
		await bot.say("Shutting down...")
		sys.exit()
	else:
		await bot.say("**ERROR**")
		await bot.say(permission_error_message)

		
#Lists the questions
@bot.command(help="lists all questions found in the surveys file and numbers them for use with other commands",brief="find the questions")
async def questions():
	await bot.say("---Short Answer Questions---")
	for i in surveys:
		message=str("**Question#" + str(surveys.index(i)) + "** " + i)
		await bot.say(message)
	await bot.say("---Multiple Choice Questions---")
	for i in surveys2:
		message=str("**Question#" + str(surveys.index(i)) + "** " + i)

#answers the question
@bot.command(help="first argument must be the question number, followed by your answer",brief="to answer questions", pass_context = True)
async def answer(ctx, number, *args):
	try:
		int(number)
	except ValueError:
		await bot.say("**ERROR**")
		await bot.say(number_error_message)
	else:
		response=""
		for i in args:
			response=response + " " + i
		found = False
		for i in surveys:
			if int(number) == int(surveys.index(i)):
				message = "Survey: " + number + " Recorded!"
				await bot.say(message)
				found = True
		if found == False:
			await bot.say("There isn't a survey with that number. Try again and use !questions to find the question you want to answer")
		else:
			Path=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',number)
			responseData=fetchResponses(Path)
			if responseData != "Error":
				
				responseFile=open(Path,"w+")
				
				d = {}
				print(ctx.message.author," answered question",number,"with response: ",response)
				for i in responseData[1::2]:
					
					try:
						d[i] = responseData[responseData.index(i)+1]
					except IndexError:
						pass
				if str(i) == str(ctx.message.author):
					d[i]=response
					await bot.say("*response has been changed*")
				else:
					d[str(ctx.message.author)] = response
				print (d)
				for i in d:
					responseFile.write("\n")
					responseFile.write(str(i))
					responseFile.write("\n")
					responseFile.write(d[str(i)])
				responseFile.close()
			else:
				await bot.say(file_not_found_message)
#lists responses with author name
@bot.command(help="Returns data from a given response file for a question. Number is the number of the question and should be found by using !questions",brief="list individual responses")
async def responses(number):
	Path=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',number)
	responseData=fetchResponses(Path)
	try:
		int(number)
	except ValueError:
		await bot.say("**ERROR**")
		await bot.say(number_error_message)
	else:
		if responseData != "Error":
			responseData.remove("")
			d = {}
			for i in responseData[0::2]:
				try:
					d[i]=responseData[(responseData.index(i)+1)]
				except IndexError:
					pass
			message="**Question:** " + str(surveys[int(number)])
			await bot.say(message)
			for i in d:
				message=str("**Name:** " + i + "  **Answer:** " + d[i])
				await bot.say(message)
		else:
			await bot.say("**ERROR**")
			await bot.say(file_not_found_message)
#lists responses and groups by response (don't include user names)
@bot.command(help="Returns frequency of all responses for a given question. Number is the number of the question and shuld be found by using !questions",brief="lists frequency of responses without author names")
async def totalresponses(number):
	Path=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',number)
	responseData=fetchResponses(Path)
	if responseData != "Error":
		responseData.remove("")
		try:
			int(number)
		except ValueError:
			await bot.say("**ERROR**")
			await bot.say(number_error_message)
		else:
			d = {i:responseData.count(i) for i in responseData[1::2]}
		await bot.say("**Responses** -> **Volume of response**")
		for i in d:
			message=str(i) + " **->**" + str(d[i])
			await bot.say(message)
	else:
		await bot.say("**ERROR**")
		await bot.say(file_not_found_message)
#adds a question to the surveys.txt list and creates a response file for it
@bot.command(help="Requires administration role to access. Make sure to check if your question already exists before trying to create it.",brief="to add a short answer question", pass_context = True)
async def addshortanswer(ctx, *args):
	if 'utopians' in (y.name.lower() for y in ctx.message.author.roles):
		question=""
		for i in args:
			question=question + " " + i
		overlap=False
		for i in surveys:
			if question == i:
				await bot.say("That is already a question")
				overlap=True
		if overlap != True:
			surveywrite=open(r'C:\Users\User\Desktop\program crap\discordSurvey\surveys.txt',("w"))
			surveys.append(question)
			for i in surveys:
				surveywrite.write("\n")
				surveywrite.write(str(i))
				Path=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',str(surveys.index(i)))
				tempFile=open(Path,"a+")
				tempFile.close()
			surveywrite.close()
		await bot.say("Question added")
		print(str(ctx.message.author),"Created a question.")
	else:
		await bot.say("**ERROR**")
		await bot.say(permission_error_message)
		print(str(ctx.message.author),"Tried to add a question without permission.")

#@bot.command(pass_context=True, help="Requires administration to access. start with the question (put in parenthesis) and then list each possible response (also in parenthesis if multiple words)",brief="Adds multiple choice question")
#async def addmultiplechoice(ctx, question, *args):
#	if 'utopians' in (y.name.lower() for y in ctx.message.author.roles):
#		choices=[]
#		for i in args:
#			choices.append(i)
#		for i in surveys2:
#			if question == i:
#				await bot.say("That is already a question.")
#				overlap=True
#		if overlap != True:
#			surveys2.append(question)
#			surveywrite2=open(r'C:\Users\User\Desktop\program crap\discordSurvey\surveys2.txt',("w"))
#			for i in surveys2:
#				surveywrite2.write("\n")
#				surveywrite2.write(str(i))
#			surveywrite2.close()
#			Path=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',str(surveys2.index(surveys2.index(question))),"_mc")
#			file=open(Path,"a+")
#			for i in choices:
#				file.write(i)
#				file.write("-")
#			file.truncate()
					


		
#removes a question from the surveys.txt file and removes it's response file. Also sorts the other questions so there isn't a gap where the question was removed
@bot.command(help="Requires administration role to access. Make sure to check that your question exists before you try to delete it, and that you get the number of it and not the actual text. Use !questions to find the number of the question you wish to remove",brief="to remove a question", pass_context = True)
async def removequestion(ctx, question):
	if 'utopians' in (y.name.lower() for y in ctx.message.author.roles):
		try:
			int(question)
		except ValueError:
			await bot.say("**ERROR**")
			await bot.say(number_error_message)
		else:
			found=False
			for i in surveys:
				if int(question) == surveys.index(i):
					await bot.say("Question found...")
					Overlap=True
					Path=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',str(surveys.index(i)))
					os.remove(Path)
					found=True
					surveys.remove(i)
					await bot.say("and deleted")
			if found == False:
				await bot.say("question not found")
			else:
				surveywrite=open(r'C:\Users\User\Desktop\program crap\discordSurvey\surveys.txt',("w"))
				for i in surveys:
					surveywrite.write("\n")
					surveywrite.write(str(i))
				surveywrite.close()
				for i in surveys:
					if int(question) <= surveys.index(i):
						Path1=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',str(surveys.index(i)+1))
						Path2=path.join(r'C:\Users\User\Desktop\program crap\discordSurvey\responses',str(surveys.index(i)))
						os.rename(Path1,Path2)
	else:
		await bot.say("**ERROR**")
		await bot.say(permission_error_message)
		
		
bot.run('MzU3NjI0NjY5MzY2NTE3Nzcz.DLQCKQ.xn71e2lyw2Hu4zWwILWfLNzFZVI')