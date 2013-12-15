import os
# very rough:

def translated(ifile):
    """ this high level routine defines the all the
    steps as necessary to translate any individual test
    document into up to two lines in our final file """

    file = open('./raw/%s' % ifile, 'r')
    raw = file.read()
    lines = raw.split('\n')
    file.close()
    print 'loaded ./raw/%s for etl; found %u lines\n' % (ifile, len(lines))
    
    required = {
        'year': False,
        'sex': False,
        'doctor': False,
        'habit': False,
        'height': False,
        'weight': False
    }
    
    for line in lines:
        (stat, val) = find_stat_in(line)
        if not stat:
            continue
        if stat in required and val:
            required[stat] = val

    for req in required:
        if not required[req]:
            return False
    
    return '%u,%s,%s,%s,%s,%f,%f' % (
        required['year'],
        required['sex'],
        required['doctor'],
        required['habit'],
        required['height'],
        weight['weight']
    )


def find_stats_in(line):
    """ this encapsulated series of tests checks each line provided
    for indications that it matches an expected variety of element """
    
    if year_found_in(line):
        return ('year', int(line))
        
    if gender_found_in(line):
        return ('sex', line.upper()[0])
        
    if doctor_found_in(line):
        return ('doctor', str(line))
        
    if quantity_and_years_found_in(line):
        return ('habit', '%u,%u' % separate_quantity_and_years_from(line))
    elif quantity_found_in(line):
        return ('habit', '%u,0' % separate_quantity_from(line))
    elif years_found_in(line):
        return ('habit', '0,%u' % separate_years_from(line))

    if height_found_in(line):
        return ('height' % separate_height_from(line))
        
    if weight_found_in(line):
        return ('weight' % separate_weight_from(line))

    return None


def year_found_in(line):
    """ this subroutine will try to find the first
    instance of a year within the raw """
    
    try:
        year = int(line)
        #TODO: test that it is a reasonable year
        return True
    except:
        return False
   
    
def gender_found_in(line):
    """ this subroutine will try to find the first
    instance of a gender within the raw """
    
    if line in ('m','M','male','Male','MALE','f','F','female','Female','FEMALE'):
        return True
    return False

    
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

    line = '%s,%u,%u,%s,%s,%u,%u,%f,%u,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'

    return []
    
def raw_directory():
    """ walk the contents of the ./raw directory, 
    load each in kind, and return it! """

    files = []
    for file in os.listdir('./raw'):
        if file.endswith('.txt') or file.endswith('.TXT'):
            files.append(file)
    return files

if __name__ == "__main__":
    out = open('tests.csv', 'w')
    out.write('ID,DOB,Age,Sex,Doc,Years,Quantity,Height,Weight,PrePost,FVCPred,FVC1,FVC2,FVC3,FVC4,FVC5,FVCG,FVCH,FVCD,FEV1Pred,FEV11,FEV12,FEV13,FEV14,FEV15,FEV1G,FEV1H,FEV1D\n')
    for ifile in raw_directory():
        for record in translated(ifile):
            out.write(record)
