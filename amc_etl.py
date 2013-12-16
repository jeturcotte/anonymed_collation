import os
import re
# very rough:

def translated(ifile):
    """ this high level routine defines the all the
    steps as necessary to translate any individual test
    document into up to two lines in our final file """
    
    required = {
        'year': False,
        'sex': False,
        'doctor': False,
        'habit': False,
        'height': False,
        'weight': False
    }
 
    file = open('./raw/%s' % ifile, 'r')
    lines = file.readlines()
    for line in lines:
        (stat, val) = find_stat_in(line.upper().strip('\r\n'))
        if not stat:
            continue
        if stat in required and val:
            required[stat] = val

    file.close()

    for req in required:
        if not required[req]:
            print 'FAIL: %s not found in :: (%s)' % (req, ifile)
            return []
    
    return '%u,%s,%s,%s,%f,%f' % (
        required['year'],
        required['sex'],
        required['doctor'],
        required['habit'],
        required['height'],
        required['weight']
    )


def find_stat_in(line):
    """ this encapsulated series of tests checks each line provided
    for indications that it matches an expected variety of element """
    
    if year_found_in(line):
        return ('year', int(line))
        
    if gender_found_in(line):
        return ('sex', line.upper()[0])
        
    if doctor_found_in(line):
        return ('doctor', str(line))
    
    if good_habit_found_in(line):
        return ('habit','0,0')
    elif quantity_and_years_found_in(line):
        return ('habit', '%u,%u' % separate_quantity_and_years_from(line))
    elif quantity_found_in(line):
        return ('habit', '%u,0' % extract_integer_from(line))
    elif years_found_in(line):
        return ('habit', '0,%u' % extract_integer_from(line))

    if height_found_in(line):
        return ('height', extract_float_from(line))
        
    if weight_found_in(line):
        return ('weight', extract_float_from(line))

    return (None, None)


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
    
    return True if line in ('M','MALE','F','FEMALE') else False

    
def doctor_found_in(line):
    """ this subroutine will try to find the first
    instance of a doctor within the raw """
    
    return True if line.startswith('DR') else False


def good_habit_found_in(line):
    """ in the event that the patient has never smoken """
    
    return True if line.startswith('NEVER') else False
    
    
def quantity_and_years_found_in(line):
    """ information about how much and how long a person
    in the study has smoked appear to be fairly hit or miss
    so this routine is meant to determine if both have
    been provided; extraction occurs elsewhere """
    
    return True if line.startswith('X') else False


def separate_quantity_and_years_from(line):
    """ this routine extracts the numerics from a line
    that contains both stats re: how much and how long """
       
    try:
        (years, quant) = [int(s) for s in line.split() if s.isdigit()]
        return (years, quant)
    except:
        print 'ERROR: years/quant not in :: (%s)' % line
        return (0,0)
        

def quantity_found_in(line):
    """ check the line to see if, at the very least, a 
    number of cigarettes per year is indicated """
    
    return True if line.startswith('X ') else False
        
    
def years_found_in(line):
    """ finally check to see if merely the years of a habit
    are listed in this line """
    
    return True if line.endswith('YEARS') or line.endswith('HISTORY') else False
        
    
def extract_integer_from(line):
    """ if we are expecting a single integer in a line,
    let us then extract and conver it """
    
    digits = re.findall('\d+', line)
    if len(digits) > 1:
        print 'ERROR: more than one integer found in :: %s\n' % line
    if not len(digits):
        print 'ERROR: no integers found in :: (%s)' % line
    return int(digits[0])
    
    
def extract_float_from(line):
    """ if we are expecting a single float in a line,
    let us then extract and convert it """
    
    floats = re.findall('\d+.\d+', line)
    if len(floats) > 1:
        print 'ERROR: more than one float found in:: %s\n' % line
    if not len(floats):
        print 'ERROR: no floats found in :: (%s)' % line
        
    
def height_found_in(line):
    """ this subroutine will try to find the first
    instance of a height (in cm) in the raw """
    
    return True if line.endswith('CM') else False

    
def weight_found_in(line):
    """ this subroutine will try to find the first 
    instance of a weight (in kg) in the raw """
    
    return True if line.endswith('KG') else False
    

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
            print record
            out.write(record)
