import pandas as pd
import pytest
import operator
from csgo.analytics.statistics import (extract_numeric_filters,check_filters,logical_operation,filter_dataframe,calculate_statistics)

class TestStatistics:
    """Class to test the five statistics functions"""
    
    def setup_class(self):
        """Setup class by defining filters and dataframes"""
        self.df=pd.DataFrame({"PlayerName":["Player1","Player2","Player3","Player4","Player5"],
                              "Kills":[5,10,15,20,25],
                              "Defused Bomb":[True,False,True,False,False]})
        self.filters={"PlayerName":["Player1","Player2","Player3"],"Kills":[">=10","<=20"],"Defused Bomb":[True]}
        self.filtered_df=pd.DataFrame({"PlayerName":["Player3"],"Kills":["==15"],"Defused Bomb":[True]})        
        self.invalid_numeric_filters={"Kills":[10]}
        self.invalid_logical_operator={"Kills":["=invalid=10"]}
        self.invalid_numeric_value={"Kills":["==1invalid0"]}
        self.invalid_str_filters={"PlayerName":[1]}
        self.invalid_bool_filters={"Defused Bomb":["True"]}
        self.statistics_df=pd.DataFrame({"AttackerName":["Player1","Player1","Player1","Player2","Player2","Player2"],
                                         "AttackerAreaId":[1,1,1,2,1,1],
                                         "Weapon":["Pistol","Melee","Pistol","Pistol","Pistol","Pistol"],
                                         "IsHeadshot":[True,False,True,False,False,True]})
        self.statistics_filters={"AttackerAreaId":["==1"],"Weapon":["Pistol"],"IsHeadshot":[True]}
        self.calculated_df=pd.DataFrame({"PlayerName":["Player1","Player2"],
                                         "Area 1 Pistol Headshot Kills":[2,1]})

    def test_extract_numeric_filters(self):
        """Test extract_numeric_filters function"""
        assert extract_numeric_filters({"Kills":["==15"]},"Kills")==(["=="],[15.0])
        assert extract_numeric_filters({"Kills":["!=15"]},"Kills")==(["!="],[15.0])
        assert extract_numeric_filters({"Kills":["<=15"]},"Kills")==(["<="],[15.0])
        assert extract_numeric_filters({"Kills":[">=15"]},"Kills")==([">="],[15.0])
        assert extract_numeric_filters({"Kills":["<15"]},"Kills")==(["<"],[15.0])
        assert extract_numeric_filters({"Kills":[">15"]},"Kills")==([">"],[15.0])
        assert extract_numeric_filters({"Kills":[">10","<20"]},"Kills")==([">","<"],[10.0,20.0])
        
    def test_extract_numeric_filters_invalid_type(self):
        """Test extract_numeric_filters function with invalid numeric filters"""
        with pytest.raises(ValueError):
            extract_numeric_filters(self.invalid_numeric_filters,"Kills")
            
    def test_extract_numeric_filters_invalid_operator(self):
        """Test extract_numeric_filters function with an invalid logical operator in the numeric filters"""
        with pytest.raises(Exception):
            extract_numeric_filters(self.invalid_logical_operator,"Kills")
            
    def test_extract_numeric_filters_invalid_numeric_value(self):
        """Test extract_numeric_filters function with an invalid numeric value in the the numerical filters"""
        with pytest.raises(Exception):
            extract_numeric_filters(self.invalid_numeric_value,"Kills")
   
    def test_check_filters_invalid_str_filters(self):
        """Test check_filters function with invalid string filters"""
        with pytest.raises(ValueError):
            check_filters(self.df,self.invalid_str_filters)
            
    def test_check_filters_invalid_bool_filters(self):
        """Test check_filters function with invalid boolean filters"""
        with pytest.raises(ValueError):
            check_filters(self.df,self.invalid_bool_filters)
            
    def test_logical_operation(self):
        """Test logical_operation function"""
        assert logical_operation(self.df,"Kills","==",15.0)==self.df.loc[self.df["Kills"]==15]
        assert logical_operation(self.df,"Kills","!=",15.0)==self.df.loc[self.df["Kills"]!=15]
        assert logical_operation(self.df,"Kills","<=",15.0)==self.df.loc[self.df["Kills"]<=15]
        assert logical_operation(self.df,"Kills",">=",15.0)==self.df.loc[self.df["Kills"]>=15]
        assert logical_operation(self.df,"Kills","<",15.0)==self.df.loc[self.df["Kills"]<15]
        assert logical_operation(self.df,"Kills",">",15.0)==self.df.loc[self.df["Kills"]>15]
        
    def test_filter_dataframe(self):
        """Test filter_dataframe function"""
        assert filter_dataframe(self.df,self.filters).equals(self.filtered_df)
        
    def test_calculate_statistics(self):
        """Test calculate_statistics function"""
        assert calculate_statistics(self.statistics_df,self.statistics_filters,["AttackerName"],["AttackerName"],[["count"]],["PlayerName","Area 1 Pistol Headshot Kills"]).equals(self.calculated_df)