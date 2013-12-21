import os
import re
from datetime import date
definition = 'ID,DOB,Age,Sex,Doc,Years,Quantity,Height,Weight,PrePost,FVCPred,FVC1,FVC2,FVC3,FVC4,FVC5,FVCG,FVCH,FVCD,FEV1Pred,FEV11,FEV12,FEV13,FEV14,FEV15,FEV1G,FEV1H,FEV1D\n'
structure = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
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
    
    predat = dict()
    postdat = dict()
 
    file = open('./raw/%s' % ifile, 'r')
    lines = file.readlines()
    file.close()
    
    for line in lines:
        (stat, val) = find_stat_in(line.upper().strip('\r\n'), required)
        
        if stat:
            required[stat] = val
        else:
            (test, pre, post) = find_data_in(line.upper().strip('\r\n').replace('\t','!'))
            if pre:
                predat[test] = pre
            if post:
                postdat[test] = post

    for req in required:
        if not required[req]:
            print 'FAIL: %s not found in :: (%s)' % (req, ifile)
            return (None, None)
                
    if not predat:
        print 'FAIL: no PRE data found in (%s)' % (ifile)
        return (None, None)

    finalpre = structure % (
        ifile.strip('.TXT'),
        required['year'],
        date.today().year - int(required['year']),
        required['sex'],
        required['doctor'],
        required['habit'],
        required['height'],
        required['weight'],
        predat['FVC']['pred'],
        predat['FVC']['pre1'],
        predat['FVC']['pre2'],
        predat['FVC']['pre3'],
        predat['FVC']['pre4'],
        predat['FVC']['pre5'],
        'TODO','TODO','TODO',
        predat['FEV1']['pred'],
        predat['FEV1']['pre1'],
        predat['FEV1']['pre2'],
        predat['FEV1']['pre3'],
        predat['FEV1']['pre4'],
        predat['FEV1']['pre5'],
        'TODO','TODO','TODO'
    )
    
    if postdat:
        finalpost = structure % (
            ifile.strip('.TXT'),
            required['year'],
            date.today().year - int(required['year']),
            required['sex'],
            required['doctor'],
            required['habit'],
            required['height'],
            required['weight'],
            postdat['FVC']['pred'],
            postdat['FVC']['post1'],
            postdat['FVC']['post2'],
            postdat['FVC']['post3'],
            postdat['FVC']['post4'],
            postdat['FVC']['post5'],
            'TODO','TODO','TODO',
            postdat['FEV1']['pred'],
            postdat['FEV1']['post1'],
            postdat['FEV1']['post2'],
            postdat['FEV1']['post3'],
            postdat['FEV1']['post4'],
            postdat['FEV1']['post5'],
            'TODO','TODO','TODO'
        )
        
        print finalpost
        print finalpre
        
        return (finalpre, finalpost)
        
    return (finalpre, None)


def find_stat_in(line, required):
    """ this encapsulated series of tests checks each line provided
    for indications that it matches an expected variety of element """

    if year_found_in(line):
        return ('year', int(line))
        
    if gender_found_in(line):
        return ('sex', line[0])
        
    if doctor_found_in(line) and not required['doctor']:
        return ('doctor', line)
    
    if good_habit_found_in(line):
        return ('habit','0,0')
    elif quantity_or_years_found_in(line):
        return ('habit', '%s,%s' % separate_quantity_and_years_from(line.replace('/',' ')))

    if height_found_in(line):
        return ('height', extract_numeric_from(line))
        
    if weight_found_in(line):
        return ('weight', extract_numeric_from(line))

    return (None, None)


def year_found_in(line):
    """ this subroutine will try to find the first
    instance of a year within the raw """
    
    year = re.search('(^\d\d\d\d)', line)

    return True if year else False
   
    
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
    
    
def quantity_or_years_found_in(line):
    """ information about how much and how long a person
    in the study has smoked appear to be fairly hit or miss
    so this routine is meant to determine if both have
    been provided; extraction occurs elsewhere """
    
    years = re.findall('[\s/]YEARS?', line)
    days = re.findall('[\s/]DAYS?', line)
    
    return True if years or days else False


def separate_quantity_and_years_from(line):
    """ this routine extracts the numerics from a line
    that contains both stats re: how much and how long """
    
    y = re.search('(\d+)[\s/]+YEARS?',line)
    q = re.search('(\d+)[\s/]+DAYS?',line)
    
    if not y and not q:
        print 'ERROR: years/quant not in :: (%s)' % line
    
    years = int(y.group(1)) if y else -1
    quant = int(q.group(1)) if q else -1
    
    return (years, quant)
    
    
def extract_numeric_from(line):
    """ if we are expecting a single numeric from the line """
    
    one_float = re.search('(\d+\.\d+)', line)
    if one_float:
        return one_float.group(1)
        
    one_integer = re.search('(\d+)', line)
    if one_integer:
        return one_integer.group(1)
        
    #print 'ERROR: neither int nor float found in :: (%s)\n' % line
    return ''
        
    
def height_found_in(line):
    """ this subroutine will try to find the first
    instance of a height (in cm) in the raw """
    
    return True if line.endswith('CM') else False

    
def weight_found_in(line):
    """ this subroutine will try to find the first 
    instance of a weight (in kg) in the raw """
    
    return True if line.endswith('KG') else False


def find_data_in(line):
    """ this set of test routines expect to find lines full of 
    mutliple data points to grab, as well as respond to the
    potentiality that two distinct sets of data be return """

    looking_for = ['test', 'units', 'pred', 'pre1', 'pre2', 'pre3', 'pre4', 'pre5', 'post1', 'post2', 'post3', 'post4', 'post5']
    final_pre = dict()
    final_post = dict()
    test = None
    
    the_line = line.split('!')
    if len(the_line) <= 1:
        return (None, None, None)
    for found in the_line:
            
        found = found.strip(' ')
        try:
            field = looking_for.pop(0)
        except:
            print 'WARNING: ran out of expected results'
            return (test, final_pre, final_post)
            
        if field == 'test' and found not in ['FEV1','FVC']:
            return (test, None, None)
        elif field == 'test':
            # we need to be able to send back WHICH test this line is
            test = found
                
        if field.startswith('pre') and field != 'pred':
            final_pre[field] = extract_numeric_from(found)
        elif field.startswith('post'):
            final_post[field] = extract_numeric_from(found)
        else:
            final_pre[field] = found
            final_post[field] = found
                
    return (test, final_pre, final_post)
            
    
def raw_directory():
    """ walk the contents of the ./raw directory, 
    load each in kind, and return it! """

    files = []
    for file in os.listdir('./raw'):
        if file.upper().endswith('.TXT'):
            files.append(file)
    return files


if __name__ == "__main__":
    out = open('tests.csv', 'w')
    out.write('ID,DOB,Age,Sex,Doc,Years,Quantity,Height,Weight,PrePost,FVCPred,FVC1,FVC2,FVC3,FVC4,FVC5,FVCG,FVCH,FVCD,FEV1Pred,FEV11,FEV12,FEV13,FEV14,FEV15,FEV1G,FEV1H,FEV1D\n')
    for ifile in raw_directory():
        for record in translated(ifile):
            out.write(record)
