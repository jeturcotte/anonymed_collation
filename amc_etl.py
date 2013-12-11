
# very rough:

def translated(ifile):
    """ this high level routine defines the all the
    steps as necessary to translate any individual test
    document into up to two lines in our final file """

    file = open(ifile, 'r')
    raw = file.read()
    file.close()

    lines = []

    (born, sex, doc, years, quant, height, weight, raw_remaining) = find_personal_stats_in(raw)
    if not raw_remaining:
        print 'failed to process file: %s' % ifile
        return []

    for processed_line in process_tests_in(raw_remaining):
        lines.append(processed_line)

    return lines

def find_personal_stats_in(raw):
    """ this subroutine breaks down and removes the
    beginning portion of the raw file while seeking
    out identifying information that may not always
    be equally separated out but should at least
    always be present """

    try:
        (year, raw) = find_year_in(raw)
        (sex, raw) = find_gender_in(raw)
        (doc, raw) = find_doctor_in(raw)
        (years, quant, raw) = find_habit_in(raw)
        (height, raw) = find_height_in(raw)
        (weight, raw) = find_weight_in(raw)
        raw = cull_extras_from(raw)
    except Exception, e:
        print 'error: %s' % e
        return (None, None, None, None, None, None, None)

    return (year, sex, doc, years, quant, weight, raw)

def find_year_in(raw):
    """ this subroutine will try to find the first
    instance of a year within the raw """
    
    return (None, raw)
    
def find_gender_in(raw):
    """ this subroutine will try to find the first
    instance of a gender within the raw """
    
    return (None, raw)
    
def find_doctor_in(raw):
    """ this subroutine will try to find the first
    instance of a doctor within the raw """
    
    return (None, raw)
    
def find_habit_in(raw):
    """ this subroutine will try to find and
    correctly parse notes about a patient's
    habits from within the raw """
    
    return (None, None, raw)
    
def find_height_in(raw):
    """ this subroutine will try to find the first
    instance of a height (in cm) in the raw """
    
    return (None, raw)
    
def find_weight_in(raw):
    """ this subroutine will try to find the first 
    instance of a weight (in kg) in the raw """
    
    return (None, raw)
    
def cull_extras_from(raw):
    """ so as not to confuse the data parsing routines
    this subroutine will attempt to isolate only the portion
    of the raw that contains that data """
    
    return raw

def process_tests_in(raw):
    """ this subroutine runs through the FEV1, FVC, 
    FEV1/FEV, FEV1/VC, and PEF lines, determines
    if there is also a post stage, and returns 1
    or 2 fully vetted lines in response """

    line = '%s,%u,%u,%s,%s,%u,%u,%f,%u,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f'

    return []

if __name__ == "__main__":
    out = open('tests.csv', 'w')
    out.write('ID,DOB,Age,Sex,Doc,Years,Quantity,Height,Weight,PrePost,FVCPred,FVC1,FVC2,FVC3,FVC4,FVC5,FVCG,FVCH,FVCD,FEV1Pred,FEV11,FEV12,FEV13,FEV14,FEV15,FEV1G,FEV1H,FEV1D')
    for ifile in raw_directory():
        for record in translated(ifile)
            out.write(record)
