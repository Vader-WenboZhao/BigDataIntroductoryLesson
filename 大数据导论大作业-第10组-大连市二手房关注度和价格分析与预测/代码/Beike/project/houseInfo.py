class HouseInfo:                            #二手房信息
    def setFavCount(self, favCount):
        self.favCount = favCount

    def setPrice(self, totalPrice, totalUnit, unitPrice, unitPriceUnit):
        self.totalPrice = totalPrice
        self.totalUnit = totalUnit
        self.unitPrice = unitPrice
        self.unitPriceUnit = unitPriceUnit

    def setSimpleInfo(self, roomMainInfo, roomSubInfo, typeMainInfo, typeSubInfo, areaMainInfo, areaSubInfo):
        self.roomMainInfo = roomMainInfo
        self.roomSubInfo = roomSubInfo
        self.typeMainInfo = typeMainInfo
        self.typeSubInfo = typeSubInfo
        self.areaMainInfo = areaMainInfo
        self.areaSubInfo = areaSubInfo

    def setSubInfo(self, dictionary):
        self.subInfo = dictionary

    def setBaseInfo(self, dictionary):
        self.baseInfo = dictionary

    def setHouseFeature(self, dictionary):
        self.houseFeature = dictionary

    def setHouseLayout(self, dictionary):
        self.houseLayout = dictionary

    def strSubInfo(self):
        l = list(self.subInfo.keys())
        s = ""
        for i in l:
            s = s + str(i) + ":" + str(self.subInfo[i]) + "$"
        return s

    def strBaseInfo(self):
        l = list(self.baseInfo.keys())
        s = ""
        for i in l:
            s = s + str(i) + ":" + str(self.baseInfo[i]) + "$"
        return s

    def strHouseFeature(self):
        l = list(self.houseFeature.keys())
        s = ""
        for i in l:
            s = s + str(i) + ":" + str(self.houseFeature[i]) + "$"
        return s

    def strHouseLayout(self):
        l = list(self.houseLayout.keys())
        s = ""
        for i in l:
            s = s + str(i) + ":" + str(self.houseLayout[i]) + "$"
        return s

    def __str__(self):
        return str(self.favCount) + "\n" + str(self.totalPrice) + str(self.totalUnit) + "\n" + str(
            self.unitPrice) + str(self.unitPriceUnit) + "\n" + str(self.roomMainInfo) + "\n" + str(
            self.roomSubInfo) + "\n" + str(self.typeMainInfo) + "\n" + str(self.typeSubInfo) + "\n" + str(
            self.areaMainInfo) + "\n" + str(
            self.areaSubInfo) + "\n" + self.strSubInfo() + "\n" + self.strBaseInfo() + "\n" + self.strHouseFeature() + "\n" + self.strHouseLayout()
