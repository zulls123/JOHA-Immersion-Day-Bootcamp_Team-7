 const PredictiveModelAPI = {
    getResults() {
        return [{
            scenario: "test",
            raw1: 163.7923580747738,
            raw2: 26544.97556439177,
            raw3_1: 46504.37841701285,
            raw3_2: 40621.50420590696,
            weightByproductToUnit2: 0.5168331431833619,
            weightByproductToUnit3: 0.6387546803352226,
            product1Production: 12.43648148704605,
            product2Production: 3.6786884171466343,
            product3Production: 2.280498641472164,
            byproductProduction: -7.643484203537106,
            totalRevenue: 13060.909269385442,
            product1Revenue: 12000.0,
            product1OverProductionCost: 21.824074352302514,
            product1UnderProductionCost: -0.0,
            product2Revenue: 735.7376834293268,
            product2OverProductionCost: -0.0,
            product2UnderProductionCost: 321.3115828533657,
            product3Revenue: 1000.0,
            product3OverProductionCost: 560.9972829443279,
            product3UnderProductionCost: -0.0,
            excessByproductCost: -229.3045261061132
        }];
    }
}

export default PredictiveModelAPI;