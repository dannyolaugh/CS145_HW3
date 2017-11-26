# =======================================================================
import sys
import math
# =======================================================================
class DataPoints:
    # -------------------------------------------------------------------
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.isAssignedToCluster = False
    # -------------------------------------------------------------------
    def __key(self):
        return (self.label, self.x, self.y)
    # -------------------------------------------------------------------
    def __eq__(self, other):
        return self.__key() == other.__key()
    # -------------------------------------------------------------------
    def __hash__(self):
        return hash(self.__key())
    # -------------------------------------------------------------------
    @staticmethod
    def getMean(clusters, mean):
        # Initialize the mean for each cluster
        # ****************Please Fill Missing Lines Here*****************

        i = 0
        for cluster in clusters:
            cx = 0
            cy = 0
            for point in cluster:
                cx += point.x
                cy += point.y

            size = len(cluster)
            if size > 0:
                cx = (cx / size)
                cy = (cy / size)

            mean[i] = [cx, cy]
            i = i + 1

        pass
    # -------------------------------------------------------------------
    @staticmethod
    def getStdDeviation(clusters, mean, stddev):
        # Initialize the std for each cluster
        # ****************Please Fill Missing Lines Here*****************
        i = 0

        for cluster in clusters:
            numeratorx = 0
            numeratory = 0
            for point in cluster:
                numeratorx += (point.x - mean[i][0]) ** 2
                numeratory += (point.y - mean[i][1]) ** 2
            stddevx = math.sqrt(numeratorx/len(cluster))
            stddevy = math.sqrt(numeratory/len(cluster))

            stddev[i] = [stddevx, stddevy]
            i = i + 1
        pass
    # -------------------------------------------------------------------
    @staticmethod
    def getCovariance(clusters, mean, stddev, cov):
        # Initialize the cov for each cluster
        # ****************Please Fill Missing Lines Here*****************
        #summation over i of (x - meanx)(y-meany)
        i = 0
        covxy = 0
        for cluster in clusters:
            for point in cluster:
                covxy += (point.x - mean[i][0])*(point.y - mean[i][1]) #/(len(cluster) - 1)
            if (len(cluster)- 1) > 0:
                covxy = covxy/(len(cluster)-1)
            cov[i] = [[(stddev[i][0]) ** 2, covxy], [covxy, (stddev[i][1]) ** 2]]
            i = i + 1
        pass

    # -------------------------------------------------------------------
    @staticmethod
    def getNMIMatrix(clusters, noOfLabels):
        nmiMatrix = [[0 for x in range(len(clusters) + 1)] for y in range(noOfLabels + 1)]
        clusterNo = 0
        for cluster in clusters:
            labelCounts = {}
            for point in cluster:
                if not point.label in labelCounts:
                    labelCounts[point.label] = 0
                labelCounts[point.label] += 1
            max = sys.maxint
            labelNo = 0
            labelTotal = 0
            labelCounts_sorted = sorted(labelCounts.iteritems(), key=lambda (k, v): (v, k), reverse=True)
            for label, val in labelCounts_sorted:
                nmiMatrix[label - 1][clusterNo] = labelCounts[label]
                labelTotal += labelCounts.get(label)
            nmiMatrix[noOfLabels][clusterNo] = labelTotal
            clusterNo += 1
            labelCounts.clear()

        # populate last col
        lastRowCol = 0
        for i in range(len(nmiMatrix) - 1):
            totalRow = 0
            for j in range(len(nmiMatrix[i]) - 1):
                totalRow += nmiMatrix[i][j]
            lastRowCol += totalRow
            nmiMatrix[i][len(clusters)] = totalRow
        nmiMatrix[noOfLabels][len(clusters)] = lastRowCol
        return nmiMatrix
    # -------------------------------------------------------------------
    @staticmethod
    def calcNMI(nmiMatrix):
        # calculate I
        row = len(nmiMatrix)
        col = len(nmiMatrix[0])
        N = nmiMatrix[row - 1][col - 1]
        I = 0.0
        HOmega = 0.0
        HC = 0.0
        for i in range(row - 1):
            for j in range(col - 1):
                denominator = (float(nmiMatrix[i][col - 1]) * nmiMatrix[row - 1][j])
                if denominator == 0.0:
                    continue
                logPart = (float(N) * nmiMatrix[i][j]) / denominator
                if logPart == 0.0:
                    continue
                I += (nmiMatrix[i][j] / float(N)) * math.log(float(logPart))
                logPart1 = nmiMatrix[row - 1][j] / float(N)
                if logPart1 == 0.0:
                    continue
                HC += nmiMatrix[row - 1][j] / float(N) * math.log(float(logPart1))
            if float(N) == 0.0 or float(N) * math.log(nmiMatrix[i][col - 1] / float(N)) == 0.0:
                continue
            HOmega += nmiMatrix[i][col - 1] / float(N) * math.log(nmiMatrix[i][col - 1] / float(N))

        if math.sqrt(HC * HOmega) == 0.0:
            return 0.0
        return I / math.sqrt(HC * HOmega)
    # -------------------------------------------------------------------
    @staticmethod
    def getNoOFLabels(dataSet):
        labels = set()
        for point in dataSet:
            labels.add(point.label)
        return len(labels)
    # -------------------------------------------------------------------
    @staticmethod
    def writeToFile(noise, clusters, fileName):
        # write clusters to file for plotting
        f = open(fileName, 'w')
        for pt in noise:
            f.write(str(pt.x) + "," + str(pt.y) + ",0" + "\n")
        for w in range(len(clusters)):
            print("Cluster " + str(w) + " size :" + str(len(clusters[w])))
            for point in clusters[w]:
                f.write(str(point.x) + "," + str(point.y) + "," + str((w + 1)) + "\n")
        f.close()
# =======================================================================