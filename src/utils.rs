use crate::core::*;
use std::error::Error;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::prelude::*;


#[derive(Serialize)]
struct MsgSwap{
    routes: Vec<Route>,
    token_in_amount: i128,
    token_in_denom: String,
    profit: i128,
}
#[derive(Serialize)]
struct Route{
    pool_id: u32,
    token_out_denom: String,
}
#[derive(Deserialize)]
pub struct Option{
    pub denom: String,
    pub max_hop: usize,
    pub iter: i32,
    pub min_amount: i128,
    pub max_amount: i128,
}


pub fn ternary_search_tree<F: Fn(f64) -> f64>(min:f64, max:f64, iter:i32, f:F) -> (f64, f64) {
    let mut lower = min;
    let mut upper = max;

    for _ in 0..iter {
        let c1 = lower + (upper - lower)/3.;
        let c2 = upper - (upper - lower)/3.;
        if f(c2) < f(c1) {
            upper = c2;
        } else {
            lower = c1;
        }
    }
    return (lower, upper);
}

pub fn parse_pools(pools_str: &str) -> Result<HashMap<u32, Pool>, Box<dyn Error>>{
    let pools_vec: Vec<Pool> = serde_json::from_str(pools_str)?;
    let mut pools = HashMap::new();
    for pool in &pools_vec{
        pools.insert(pool.id, pool.clone());
    }
    Ok(pools)
}

pub fn get_pools_from_file() -> Result<HashMap<u32, Pool>, Box<dyn Error>> {
    let data = include_str!("../pools.json");
    let pools = parse_pools(data)?;
    Ok(pools)
}


pub fn parse_option(option_str:&String)-> Result<Option, Box<dyn Error>> {
    let option: Option = serde_json::from_str(option_str)?;
    Ok(option)
}

pub fn save_paths(paths:&Vec<Path>)-> Result<(), Box<dyn Error>>{
    let serialized = serde_json::to_string(paths)?;
    let mut file = File::create("paths.json")?;
    file.write_all(serialized.as_bytes())?;
    Ok(())
}
pub fn load_paths()-> Result<Vec<Path>, Box<dyn Error>>{
    let mut file = File::open("paths.json")?;
    let mut data = String::new();
    file.read_to_string(&mut data)?;
    let paths: Vec<Path> = serde_json::from_str(&data)?;
    Ok(paths)
}


pub fn serialize(path:&Path, amount_in:&f64, profit:&f64, denom:&String) -> String{
    let mut routes = vec![];
    for (i, denom) in path.path_denoms.iter().enumerate(){
        routes.push(Route{pool_id:path.path_pools[i], token_out_denom:denom.clone()});
    }
    let msgswap = MsgSwap{routes: routes, token_in_denom:denom.clone(), token_in_amount: *amount_in as i128, profit:*profit as i128};
    return serde_json::to_string(&msgswap).unwrap();
}


fn single_swap_output(amount_in:f64, balance_in:i128, balance_out:i128, weight_in:i128, weight_out:i128, swap_fee:f64) -> f64{
    let ratio = weight_in as f64/ weight_out as f64;
    return (balance_out as f64)*(1.0 - ((balance_in as f64)/ (balance_in as f64 + (1.0 - swap_fee)*amount_in)).powf(ratio));
}

pub fn multiple_swap_output(pools:&HashMap<u32, Pool>, path:&Path, start_denom:&String, amount_in:&f64) -> f64{
    let mut current_denom = start_denom.clone();
    let mut current_amount = *amount_in;
    for i in 0..path.path_pools.len(){
        let current_pool_id = path.path_pools[i];
        let pool = &pools[&current_pool_id];
        if current_denom==pool.denom0{
            current_denom = pool.denom1.clone();
            current_amount = single_swap_output(current_amount, pool.amount0, pool.amount1, pool.weight0, pool.weight1, pool.swap_fee);
        } else {
            assert_eq!(current_denom, pool.denom1);
            current_denom = pool.denom0.clone();
            current_amount = single_swap_output(current_amount, pool.amount1, pool.amount0, pool.weight1, pool.weight0, pool.swap_fee);
        }
    }
    assert_eq!(start_denom, &current_denom);
    return current_amount;
}

