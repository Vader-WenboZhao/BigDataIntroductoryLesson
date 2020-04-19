from project.beikePage import BeikePage


class ErshoufangPage:                       #二手房网页
    def __init__(self, pageTitle, title, sub, houseInfo):
        self.pageTitle = pageTitle
        self.title = title
        self.sub = sub
        self.houseInfo = houseInfo

    def __str__(self):
        return str(self.pageTitle) + "\n" + str(self.title) + "\n" + str(self.sub) + "\n" + str(self.houseInfo)
