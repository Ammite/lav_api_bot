from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import constants
import logging
from time import localtime, time
from timedate import Period, in_minutes, in_minutes_t, in_h_m, add_utc


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

updater = Updater(token=constants.token)

dispatcher = updater.dispatcher


def take_data():
    """

                Creating list of lessons

    """

    lessons = []
    for i in constants.lessons:
        x = Period(i[0], i[1], i[2], i[3], i[4], i[5])
        lessons.append(x)
    '''

                Takes present time

    '''
    time_now = [localtime(time())[3], localtime(time())[4]]
    time_now_day = localtime(time())[6]
    #print(time_now, time_now_day)
    time_now[0], time_now[1], time_now_day = add_utc(3, time_now[0], time_now[1], time_now_day)[0], \
                                             add_utc(3, time_now[0], time_now[1], time_now_day)[1], \
                                             add_utc(3, time_now[0], time_now[1], time_now_day)[2]
    #print(time_now, time_now_day)
    '''

                Search for the next lesson

    '''

    today_lessons = [i for i in lessons if i.day == constants.days[time_now_day]]

    lessons_now = "Nothing on today"

    trigger = True
    for i in today_lessons:
        if in_minutes_t(i.time_start) <= in_minutes(time_now[0], time_now[1]) < in_minutes_t(i.time_end):
            lessons_now = i.subject, i.kind, i.room, \
                          (in_minutes_t(i.time_end) - in_minutes(time_now[0], time_now[1])), False, i.time_start
            trigger = False

    if trigger:
        delta_time = 1440
        for i in today_lessons:
            if 0 < in_minutes_t(i.time_start) - in_minutes(time_now[0], time_now[1]) < delta_time:
                delta_time = in_minutes_t(i.time_start) - in_minutes(time_now[0], time_now[1])
                lessons_now = i.subject, i.kind, i.room, \
                              (in_minutes_t(i.time_start) - in_minutes(time_now[0], time_now[1])), True, i.time_end

    result = "Lesson: {},\nCategory: {},\nRoom: {},\n".format(lessons_now[0], lessons_now[1], lessons_now[2])
    hours_left, minutes_left = str(in_h_m(lessons_now[3])[0]), str(in_h_m(lessons_now[3])[1])
    if lessons_now[4]:
        result += "Lesson starts in {}:{},\n".format(lessons_now[5].hour, lessons_now[5].minute)
        result += "Before the beginning of the lesson " + hours_left + ":" + minutes_left + " left."
    else:
        result += "Lesson ends in {}:{},\n".format(lessons_now[5].hour, lessons_now[5].minute)
        result += "Until the end of the lesson " + hours_left + ":" + minutes_left + " left."
    return result


def echo(bot, update):
    update.message.reply_text(take_data())


def main():

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()


if __name__ == '__main__':
    main()
