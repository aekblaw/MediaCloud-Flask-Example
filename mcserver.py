import ConfigParser, logging, datetime, os, collections


from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    #now = datetime.datetime.now()
    
    #Could make these more elegant by grabbing a tuple of all three at once, rather than separately. Could include better form troubleshooting (like only allowing integers)

    startYear = int(request.form['year1'])
    print request.form['year1']
    print type(request.form['year1'])
    startMonth = int(request.form['month1'])
    startDay = int(request.form['day1'])

    endYear = int(request.form['year2'])
    endMonth = int(request.form['month2'])
    endDay = int(request.form['day2'])

    startDate = datetime.date(startYear, startMonth, startDay)
    endDate = datetime.date(endYear, endMonth, endDay)


    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( startDate, 
                                            endDate),
                     'media_sets_id:1' ],split = True, split_start_date = str(startDate), split_end_date = str(endDate))


    #sorting functionality below adapted with help from Jasmin and Penny's code

    dataPoints = results['split']


    sorting = collections.OrderedDict(sorted(dataPoints.items()))
    
    weeks = [key[:10] for key in sorting.keys()[:-3]]

    dataPointsSorted = sorting.values()[:-3]

    print dataPointsSorted
    print weeks
    
    return render_template("search-results.html", 
        keywords=keywords, sentenceCount=results['count'], data=dataPointsSorted, weeks=weeks )

if __name__ == "__main__":
    app.debug = True
    app.run()
