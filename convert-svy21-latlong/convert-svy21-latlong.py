import os
import math
import sys
import csv

class SVY21:
    # Ref: https://web.archive.org/web/20160603004136/linz.govt.nz/geodetic/conversion-coordinates/projection-conversions/transverse-mercator-preliminary-computations/index.aspx

    # WGS84 Datum
    a = 6378137
    f = 1 / 298.257223563

    # SVY21 Projection
    # Fundamental point: Base 7 at Pierce Resevoir.
    # Latitude: 1 22 02.9154 N, longitude: 103 49 31.9752 E (of Greenwich).

    oLat = 1.366666  # origin's lat in degrees
    oLon = 103.833333  # origin's lon in degrees
    oN = 38744.572  # false Northing
    oE = 28001.642  # false Easting
    k = 1  # scale factor

    def __init__(self):
        self.b = self.a * (1 - self.f)
        self.e2 = (2 * self.f) - (self.f * self.f)
        self.e4 = self.e2 * self.e2
        self.e6 = self.e4 * self.e2
        self.A0 = 1 - (self.e2 / 4) - (3 * self.e4 / 64) - (5 * self.e6 / 256)
        self.A2 = (3. / 8.) * (self.e2 + (self.e4 / 4) + (15 * self.e6 / 128))
        self.A4 = (15. / 256.) * (self.e4 + (3 * self.e6 / 4))
        self.A6 = 35 * self.e6 / 3072

    def computeSVY21(self, lat, lon):
        latR = lat * math.pi / 180
        sinLat = math.sin(latR)
        sin2Lat = sinLat * sinLat
        cosLat = math.cos(latR)
        cos2Lat = cosLat * cosLat
        cos3Lat = cos2Lat * cosLat
        cos4Lat = cos3Lat * cosLat
        cos5Lat = cos4Lat * cosLat
        cos6Lat = cos5Lat * cosLat
        cos7Lat = cos6Lat * cosLat

        rho = self.calcRho(sin2Lat)
        v = self.calcV(sin2Lat)
        psi = v / rho
        t = math.tan(latR)
        w = (lon - self.oLon) * math.pi / 180

        M = self.calcM(lat)
        Mo = self.calcM(self.oLat)

        w2 = w * w
        w4 = w2 * w2
        w6 = w4 * w2
        w8 = w6 * w2

        psi2 = psi * psi
        psi3 = psi2 * psi
        psi4 = psi3 * psi

        t2 = t * t
        t4 = t2 * t2
        t6 = t4 * t2

        # Compute Northing
        nTerm1 = w2 / 2 * v * sinLat * cosLat
        nTerm2 = w4 / 24 * v * sinLat * cos3Lat * (4 * psi2 + psi - t2)
        nTerm3 = w6 / 720 * v * sinLat * cos5Lat * (
                (8 * psi4) * (11 - 24 * t2) - (28 * psi3) * (1 - 6 * t2) + psi2 * (1 - 32 * t2) - psi * 2 * t2 + t4)
        nTerm4 = w8 / 40320 * v * sinLat * cos7Lat * (1385 - 3111 * t2 + 543 * t4 - t6)
        N = self.oN + self.k * (M - Mo + nTerm1 + nTerm2 + nTerm3 + nTerm4)

        # Compute Easting
        eTerm1 = w2 / 6 * cos2Lat * (psi - t2)
        eTerm2 = w4 / 120 * cos4Lat * ((4 * psi3) * (1 - 6 * t2) + psi2 * (1 + 8 * t2) - psi * 2 * t2 + t4)
        eTerm3 = w6 / 5040 * cos6Lat * (61 - 479 * t2 + 179 * t4 - t6)
        E = self.oE + self.k * v * w * cosLat * (1 + eTerm1 + eTerm2 + eTerm3)

        return (N, E)

    def calcM(self, lat):
        latR = lat * math.pi / 180
        return self.a * ((self.A0 * latR) - (self.A2 * math.sin(2 * latR)) + (self.A4 * math.sin(4 * latR)) - (
                self.A6 * math.sin(6 * latR)))

    def calcRho(self, sin2Lat):
        num = self.a * (1 - self.e2)
        denom = math.pow(1 - self.e2 * sin2Lat, 3. / 2.)
        return num / denom

    def calcV(self, sin2Lat):
        poly = 1 - self.e2 * sin2Lat
        return self.a / math.sqrt(poly)

    def computeLatLon(self, N, E):
        Nprime = N - self.oN
        Mo = self.calcM(self.oLat)
        Mprime = Mo + (Nprime / self.k)
        n = (self.a - self.b) / (self.a + self.b)
        n2 = n * n
        n3 = n2 * n
        n4 = n2 * n2
        G = self.a * (1 - n) * (1 - n2) * (1 + (9 * n2 / 4) + (225 * n4 / 64)) * (math.pi / 180)
        sigma = (Mprime * math.pi) / (180. * G)

        latPrimeT1 = ((3 * n / 2) - (27 * n3 / 32)) * math.sin(2 * sigma)
        latPrimeT2 = ((21 * n2 / 16) - (55 * n4 / 32)) * math.sin(4 * sigma)
        latPrimeT3 = (151 * n3 / 96) * math.sin(6 * sigma)
        latPrimeT4 = (1097 * n4 / 512) * math.sin(8 * sigma)
        latPrime = sigma + latPrimeT1 + latPrimeT2 + latPrimeT3 + latPrimeT4

        sinLatPrime = math.sin(latPrime)
        sin2LatPrime = sinLatPrime * sinLatPrime

        rhoPrime = self.calcRho(sin2LatPrime)
        vPrime = self.calcV(sin2LatPrime)
        psiPrime = vPrime / rhoPrime
        psiPrime2 = psiPrime * psiPrime
        psiPrime3 = psiPrime2 * psiPrime
        psiPrime4 = psiPrime3 * psiPrime
        tPrime = math.tan(latPrime)
        tPrime2 = tPrime * tPrime
        tPrime4 = tPrime2 * tPrime2
        tPrime6 = tPrime4 * tPrime2
        Eprime = E - self.oE
        x = Eprime / (self.k * vPrime)
        x2 = x * x
        x3 = x2 * x
        x5 = x3 * x2
        x7 = x5 * x2

        # Compute Latitude
        latFactor = tPrime / (self.k * rhoPrime)
        latTerm1 = latFactor * ((Eprime * x) / 2)
        latTerm2 = latFactor * ((Eprime * x3) / 24) * (
                (-4 * psiPrime2) + (9 * psiPrime) * (1 - tPrime2) + (12 * tPrime2))
        latTerm3 = latFactor * ((Eprime * x5) / 720) * (
                (8 * psiPrime4) * (11 - 24 * tPrime2) - (12 * psiPrime3) * (21 - 71 * tPrime2) + (
                15 * psiPrime2) * (15 - 98 * tPrime2 + 15 * tPrime4) + (180 * psiPrime) * (
                        5 * tPrime2 - 3 * tPrime4) + 360 * tPrime4)
        latTerm4 = latFactor * ((Eprime * x7) / 40320) * (1385 - 3633 * tPrime2 + 4095 * tPrime4 + 1575 * tPrime6)
        lat = latPrime - latTerm1 + latTerm2 - latTerm3 + latTerm4

        # Compute Longitude
        secLatPrime = 1. / math.cos(lat)
        lonTerm1 = x * secLatPrime
        lonTerm2 = ((x3 * secLatPrime) / 6) * (psiPrime + 2 * tPrime2)
        lonTerm3 = ((x5 * secLatPrime) / 120) * ((-4 * psiPrime3) * (1 - 6 * tPrime2) + psiPrime2 * (
                9 - 68 * tPrime2) + 72 * psiPrime * tPrime2 + 24 * tPrime4)
        lonTerm4 = ((x7 * secLatPrime) / 5040) * (61 + 662 * tPrime2 + 1320 * tPrime4 + 720 * tPrime6)
        lon = (self.oLon * math.pi / 180) + lonTerm1 - lonTerm2 + lonTerm3 - lonTerm4

        return round((lat / (math.pi / 180)),5), round(lon / (math.pi / 180),3)
    
def convert_lat_lon(lat_str, lon_str):
    # Initialize SVY21 object
    cv = SVY21()
    
    # Parse latitude and longitude from input strings
    lat = float(lat_str)
    lon = float(lon_str)
    
    # Compute latitude and longitude using SVY21
    result = cv.computeLatLon(lat, lon)
    
    return result

    
def process_user_input():
    if len(sys.argv) != 4:
        print("Usage: python convert-svy21-latlong.py --direct <x> <y>")
        sys.exit(1)
    
    # Extract latitude and longitude from command-line arguments
    input_x = sys.argv[2]
    input_y = sys.argv[3]
    
    # Call the conversion function
    result = convert_lat_lon(input_y, input_x)
    
    # Print the result
    print("Latitude:", result[0])
    print("Longitude:", result[1])

def is_csv_file(filename):
    return filename.lower().endswith(".csv")

def process_file_input(input_filename, output_filename):
    if not os.path.exists(input_filename):
        print("Input file does not exist:", input_filename)
        print("For user input use the following: python convert-svy21-latlong.py --direct <x> <y>")
        sys.exit(1)
    if not is_csv_file(input_filename):
        print("Makesure filename extension is '.csv'.")
        sys.exit(1)
    # Initialize SVY21 object
    cv = SVY21()

    # Check if the output filename has the ".csv" extension
    if not is_csv_file(output_filename):
        # If not, strip any existing extension and append ".csv" to the filename
        output_filename = os.path.splitext(output_filename)[0] + ".csv"
    
    with open(output_filename, "w", newline='') as output:
        write = csv.writer(output)
        write.writerow(["Lat", "Long"])
    
    with open(input_filename, 'r') as csvfile:
        input = csv.reader(csvfile)
        next(input)
        for row in input:
            x = float(row[0])
            y = float(row[1])
            result = cv.computeLatLon(y, x)

            with open(output_filename, "a", newline='') as output:
                write = csv.writer(output)
                write.writerow(result)

            output.close()
    
    print("Done! Check", output_filename, "file in the folder")
    csvfile.close()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # User provided input and output file names as command-line arguments
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file_input(input_file, output_file)
    elif len(sys.argv) == 4 and sys.argv[1] == "--direct":
        # User provided latitude and longitude as command-line arguments
        process_user_input()
    else:
        print("Usage: python convert-svy21-latlong.py --direct <x> <y>")
        print("       python convert-svy21-latlong.py <input_file.csv> <output_file.csv>")
        sys.exit(1)