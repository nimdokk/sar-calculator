import math
import click

#note, numbers do not need to be Metric, but for consistency, put them all in metric, do not mix Metric and Imperial

@click.group()
def cli():
    """Obtain inputs and calculate PoD from Range of Detection with Correction Factors for Low, Medium, High Visibility"""

#################### Range of Detection/AMDR calculator ###############################
@cli.group('rd')
def rd():
    """Calculate Range of Detection / AMDR"""

@rd.command('rd_calc')
def rd_calc():
    print("Get the Estimated POD Percentage")
    print("For consistency use the same distance measurements (recommend using metric)")
    print("First get the Range of Detection / AMDR for the search assignment")

    rd_list={"rd1":0,"rd2":0,"rd3":0,"rd4":0,"rd5":0,"rd6":0,"rd7":0,"rd8":0}

    for range in rd_list:
        rd_list[range]=float(input("Enter the distance in meters: "))

    #Calculate the Range of Detection - AMDR from distance inputs
    Rd=sum(rd_list.values())/len(rd_list.values())

    print("Range of Detection/AMDR (Average meters)",round(Rd,2))
    return(Rd)


######################  pod calculator  ###########################
@cli.group('pod')
def pod():
    """Calculate PoD with Correction Factors"""

@pod.command('pod_calc')
def pod_calc():

    print("Get the Estimated POD Percentage")
    print("For consistency use the same distance measurements (recommend using metric)")
    print("First get the Range of Detection / AMDR for the search assignment")

    rd_list={"rd1":0,"rd2":0,"rd3":0,"rd4":0,"rd5":0,"rd6":0,"rd7":0,"rd8":0}

    for range in rd_list:
        rd_list[range]=float(input("Enter the distance in meters: "))

    #Calculate the Range of Detection - AMDR from distance inputs
    Rd=sum(rd_list.values())/len(rd_list.values())

    print("Range of Detection/AMDR (Average meters)",round(Rd,2))


    # the correction factors for low, medium, high visibility classes
    Cf={"low":1.1,"med":1.6,"high":1.8}

    # add something so that we could prompt to deterimine if this should eb based on searchers and time or GPS/GLONASS track distance
    #Obtain the TIme spent searching - this value should in Hours
    time_searching=float(input("Enter time searching (hours): "))

    #obtain the Velocity of the searchers in km/hr
    velocity=float(input("Enter the velocity (km/hour): "))

    #number of searchers on the assigned area
    number_of_searchers=int(input("Enter the number of searchers: "))

    #enter the size of the search area - obtain from SARTopo Assignment
    A=float(input("Enter the size of the area swept (square kilometers): "))

    # To Help  determine the Probablity of Success, promt for the Probability of Area as a percentage, just enter the number
    #example: 50% just enter 50
    #POA_e=float(input("Enter the estimated Probability of Area: "))

    #convert the POA percentage to a decimal number for calculating later
    #POA=POA_e/100

    #Track Line Length = time spent searching (hours) * velocity of searchers
    TL=time_searching * velocity
    #Total Track Length = Track Line Length * number of searchers
    TTL=TL * number_of_searchers

    #print("\n")


    for key,value in Cf.items():
        #calculate sweep width for each Correction Factor
        W=Rd * Cf[key]
        #calculate area effectively swept = Total Track Length * Sweep Width
        Z=TTL * W
        #Calculate Coverage = Area effectively swept divided by the Area of the search
        C=Z/A
        #Calculate the probability of Detection = 1 minus e raised to the negative Coverage - e = Euler's Number
        POD=1 - math.exp(-C)
        print("POD Percentage for",key,"-visibility class is: ",format(POD,'.2%'))
        #for completeness - calculate the Probability of Success = POA * POD
        #POS=POA*POD
        #print("POS Percentage for",key,"-visibility class is: ",format(POS,'.2%'))
    return

if __name__ == '__main__':
    cli()

