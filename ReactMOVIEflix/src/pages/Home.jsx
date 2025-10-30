import MovieCard from "../components/MovieCard"
import { useEffect, useState } from "react";
import "../css/Home.css";
import { searchMovies,getPopularMovies  } from "../services/api";
function Home(){
    const[searchQuery,setsearchQuery]=useState("");
    const [movies,setMovies]=useState([]);
    const[error,setError]=useState(null);
    const [loading,setloading] =useState(true)
    useEffect (()=> {
        const loadPopularMovies =async () => {
            try{
                const popularMovies =await getPopularMovies()
                setMovies(popularMovies)

            }catch(err){
                console.log(err)
                setError("Failed to load movies...")
            }
            finally {
                setloading(false)
            }
        }
        loadPopularMovies()
    },[])
    const handleSearch= (e) =>{
    e.preventDefault();
    alert(searchQuery);
    };
    return(
         <div className="home">
            <form onSubmit={handleSearch} className="search-form">
            <input 
            type="text"
             placeholder="Search For movies..." 
             className="search-form"
             value={searchQuery}
             onChange={(e) => setsearchQuery(e.target.value)}
             />
             <button type="submit" className="search-button">
                Search
             </button>
            </form>
            
        <div className="movie-list">
            {movies.map(
                (movie) => 
                    movie.title.toLowerCase().startsWith(searchQuery)&& (
                <MovieCard movie={movie} key={movie.id }/> 
            ))}   
            </div>
        </div>
        );
}
export default Home;