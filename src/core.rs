use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use crate::utils::*;

#[derive(Deserialize, Debug, Clone)]
pub struct Pool{
    pub id: u32,
    pub swap_fee: f64,
    pub denom0: String,
    pub amount0: i128,
    pub weight0: i128,
    pub denom1: String,
    pub amount1: i128,
    pub weight1: i128,
}
#[derive(Debug)]
pub struct Edge{
    denom: String,
    pool_id: u32
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Path{
    pub path_denoms: Vec<String>,
    pub path_pools: Vec<u32>,
}


pub fn get_graph(pools:&HashMap<u32, Pool>) -> HashMap<String, Vec<Edge>> {
    let mut graph: HashMap<String, Vec<Edge>> = HashMap::new();
    for (_, pool) in pools {
        if ! graph.contains_key(&pool.denom0){
            graph.insert(pool.denom0.clone(), Vec::new());
        }
        if ! graph.contains_key(&pool.denom1){
            graph.insert(pool.denom1.clone(), Vec::new());
        }
        let v = graph.get_mut(&pool.denom0).unwrap();
        v.push(Edge { denom: pool.denom1.clone(), pool_id: pool.id });
        let v = graph.get_mut(&pool.denom1).unwrap();
        v.push(Edge { denom: pool.denom0.clone(), pool_id: pool.id });
    }
    return graph;
}

pub fn find_paths(graph:&HashMap<String, Vec<Edge>>, u:&String, d:&String, path_orgn:&Path, paths:&mut Vec<Path>, max_hop:&usize){
    if path_orgn.path_pools.len() >= *max_hop {
        return ();
    }
    for edge in &graph[u]{
        if !path_orgn.path_pools.contains(&edge.pool_id) {
            let mut path = path_orgn.clone();
            path.path_denoms.push(edge.denom.clone());
            path.path_pools.push(edge.pool_id);
            if edge.denom==*d {
                paths.push(path.clone());
            } else {
                find_paths(graph, &edge.denom, d, &path, paths, max_hop);
            }   
        }
    }
}

pub fn find_loops(graph:&HashMap<String, Vec<Edge>>, denom: &String, max_hop:&usize) -> Vec<Path>{
    let mut paths = vec![];
    find_paths(&graph, &denom, &denom, &Path{path_denoms:vec![], path_pools:vec![]}, &mut paths, &max_hop);
    return paths;
}


pub fn select_paths_maybe_profitable(pools:&HashMap<u32, Pool>, paths:&Vec<Path>, denom:&String, min_amount:&f64) -> Vec<Path>{
    let mut selected_paths = vec![];
    for path in paths{
        let amount_out = multiple_swap_output(&pools, path, denom, &min_amount);
        if amount_out - min_amount > 0.0{
            selected_paths.push(path.clone());
        }
    }
    return selected_paths;
}

pub fn select_paths_sufficient_capacity(pools:&HashMap<u32, Pool>, paths:&Vec<Path>, denom:&String, test_amount:&f64) -> Vec<Path>{
    let mut selected_paths = vec![];
    for path in paths{
        let amount_out = multiple_swap_output(&pools, path, denom, &test_amount);
        if amount_out  > 0.99*test_amount{
            selected_paths.push(path.clone());
        }
    }
    return selected_paths;
}

pub fn find_best_amount(pools:&HashMap<u32, Pool>, path:&Path, denom:&String, min_amount:&f64, max_amount:&f64, iter:&i32) -> (f64, f64){
    let f_profit = |amount_in:f64| multiple_swap_output(pools, path, denom, &amount_in) - amount_in;
    let (lower_amount, upper_amount) = ternary_search_tree(*min_amount, *max_amount, *iter, f_profit);
    let optimal_amount = (upper_amount + lower_amount)/2.;
    let profit = multiple_swap_output(pools, path, denom, &optimal_amount) - optimal_amount;
    return (optimal_amount, profit);
}

pub fn find_best_path_and_amount(pools:&HashMap<u32, Pool>, paths:&Vec<Path>, denom:&String, min_amount:&f64, max_amount:&f64, iter:&i32) -> (Path, f64, f64){
    let mut best_profit = f64::MIN;
    let mut best_amount = None;
    let mut best_path_index = None;

    for (i, path) in paths.iter().enumerate(){
        let (amount_in, profit) = find_best_amount(pools, path, denom, min_amount, max_amount, iter);
        if profit > best_profit{
            best_profit = profit;
            best_path_index = Some(i);
            best_amount = Some(amount_in);
        }
    }
    let amount = match best_amount {
        Some(amount) => amount,
        None => panic!(),
    };
    let path = match best_path_index {
        Some(i) => paths[i].clone(),
        None => panic!(),
    };
    return (path, amount, best_profit);
}
