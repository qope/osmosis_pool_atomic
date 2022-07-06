mod utils;
mod core;

use crate::core::*;
use utils::*;


fn main() {
    let mut denom = "uosmo".to_string();
    let mut max_hop = 3;
    let mut min_amount = 2000.;
    let mut max_amount = 10.0f64.powi(6);
    let mut iter = 10;
    let mut pools_some = None;
    let args: Vec<String> = std::env::args().collect();
    if args.len() == 2 {panic!("args should be zero or two");}
    if args.len() == 3 {
        pools_some = Some(parse_pools(&args[1]).expect("Pools parse error!"));
        let option = parse_option(&args[2]).expect("Option parse error!");
        denom = option.denom;
        max_hop = option.max_hop;
        iter = option.iter;
        min_amount = option.min_amount as f64;
        max_amount = option.max_amount as f64;
    }

    let pools = match pools_some {
        Some(pools) => pools,
        None => get_pools_from_file().unwrap()
    };
    let graph = get_graph(&pools);
    let paths = find_loops(&graph, &denom, &max_hop);
    let selected_paths = select_paths_maybe_profitable(&pools, &paths, &denom, &min_amount);
    let (path, amount, profit) = find_best_path_and_amount(&pools, &selected_paths, &denom, &min_amount, &max_amount, &iter);
    // println!("path = {:?}, amount = {}, profit = {}", path, amount, profit);
    let msg = serialize(&path, &amount, &profit, &denom);
    print!("{}", msg);
}



#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::time::Instant;
    use std::fs::{File, remove_file};
    use std::io::prelude::*;
    use super::*;

    #[test]
    fn if_the_optimal_value_is_less_than_min_returns_min() {
        let f = |x:f64| -(x+10.0).powi(2);
        let min = 1.0;
        let r = ternary_search_tree(min, 1000.0, 10, f);
        assert_eq!(min, r.0)
    }
    
    #[test]
    fn if_the_optimal_value_is_much_than_max_returns_max() {
        let f = |x:f64| -(x-10000.0).powi(2);
        let max = 1000.0;
        let r = ternary_search_tree(1.0, max, 10, f);
        assert_eq!(max, r.1)
    }

    #[test]
    fn test_get_pools_from_file() {
        get_pools_from_file().unwrap();
    }

    #[test]
    fn test_get_graph() {
        let pools = get_pools_from_file().unwrap();
        get_graph(&pools);
    }

    #[test]
    fn test_find_loops() {
        let pools = get_pools_from_file().unwrap();
        let graph = get_graph(&pools);

        let denom = "uosmo".to_string();
        let max_hop = 2;
        find_loops(&graph, &denom, &max_hop);
    }

    #[test]
    fn test_hashmap_iter() {
        let mut m = HashMap::new();
        m.insert(1, "abc");
        m.insert(2, "cfg");
        for (key, val) in &m{
            if *key==1{
                assert_eq!(val, &"abc");
            }
            if *key==2{
                assert_eq!(val, &"cfg");
            }
        }
    }
    #[test]
    fn test_multiple_swap_output() {
        let pools = get_pools_from_file().unwrap();
        let graph = get_graph(&pools);

        let denom = "uosmo".to_string();
        let max_hop = 2;
        let paths = find_loops(&graph, &denom, &max_hop);
        multiple_swap_output(&pools, &paths[0], &denom, &1000.0);
    }
    #[test]
    fn test_find_best_amount() {
        let denom = "uosmo".to_string();
        let max_hop = 2;
        let min_amount = 2000.;
        let max_amount = 1000000.0;
        let iter = 20;
        let pools = get_pools_from_file().unwrap();
        let graph = get_graph(&pools);
        let paths = find_loops(&graph, &denom, &max_hop);
        find_best_amount(&pools, &paths[0], &denom, &min_amount, &max_amount, &iter);
    }

    #[test]
    fn test_io() -> Result<(), Box<dyn std::error::Error>> {
        let s = "Hello dfad".to_string();
        let mut file = File::create("foo.txt")?;
        file.write_all(s.as_bytes())?;
        let mut file = File::open("foo.txt")?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;
        assert_eq!(contents, s);
        remove_file("foo.txt")?;
        Ok(())
    }

    #[test]
    fn test_save_and_load_paths() {
        let now = Instant::now();
        let denom = "uosmo".to_string();
        let max_hop = 2;
        let pools = get_pools_from_file().unwrap();
        let graph = get_graph(&pools);
        let paths = find_loops(&graph, &denom, &max_hop);
        let after_find_paths = now.elapsed().as_millis(); 
        save_paths(&paths).unwrap();
        let after_save_paths = now.elapsed().as_millis(); 
        let paths2 = load_paths().unwrap();
        let after_load_paths = now.elapsed().as_millis(); 
        assert_eq!(paths, paths2);
        println!("make:{} msec, save:{} msec, load: {} msec", 
        after_find_paths, 
        after_save_paths - after_find_paths,
        after_load_paths - after_save_paths);
    }

    #[test]
    fn test_select_paths_sufficient_capacity() {
        let denom = "uosmo".to_string();
        let max_hop = 4;
        let test_amount = 10.0f64.powi(6);
        let pools = get_pools_from_file().unwrap();
        let graph = get_graph(&pools);
        let paths = find_loops(&graph, &denom, &max_hop);
        let selected_paths = select_paths_sufficient_capacity(&pools, &paths, &denom, &test_amount);
        println!("Num of selected_paths = {}", selected_paths.len());
    }
}
