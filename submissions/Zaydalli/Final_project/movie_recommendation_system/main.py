from data_manager import DataManager
from auth import AuthManager
from movie_manager import MovieManager
from recommendation import RatingManager, RecommendationEngine
from utils import print_header, print_success, print_error, input_string, input_int, pause, clear_screen, Colors

def main():
    # Initialize Core Managers
    data_manager = DataManager()
    auth_manager = AuthManager(data_manager)
    movie_manager = MovieManager(data_manager)
    rating_manager = RatingManager(data_manager, movie_manager)
    recommendation_engine = RecommendationEngine(data_manager, movie_manager, rating_manager)
    
    while True:
        if not auth_manager.is_logged_in():
            print_header("MOVIE RECOMMENDATION SYSTEM")
            print(f"{Colors.BOLD}1.{Colors.ENDC} Register")
            print(f"{Colors.BOLD}2.{Colors.ENDC} Login")
            print(f"{Colors.BOLD}3.{Colors.ENDC} Exit")
            print(f"{Colors.OKCYAN}{'=' * 50}{Colors.ENDC}")
            
            choice = input_string("Select an option: ")
            
            if choice == '1':
                auth_manager.register()
                pause()
            elif choice == '2':
                auth_manager.login()
                pause()
            elif choice == '3':
                print_success("Exiting application. Goodbye!")
                break
            else:
                print_error("Invalid choice. Please select 1, 2, or 3.")
                pause()
        else:
            current_user = auth_manager.current_user
            print_header(f"WELCOME {current_user.username.upper()}")
            print(f"{Colors.BOLD}1.{Colors.ENDC} View All Movies")
            print(f"{Colors.BOLD}2.{Colors.ENDC} Search Movies")
            print(f"{Colors.BOLD}3.{Colors.ENDC} Get Recommendations")
            print(f"{Colors.BOLD}4.{Colors.ENDC} Rate a Movie")
            print(f"{Colors.BOLD}5.{Colors.ENDC} My Favorites")
            print(f"{Colors.BOLD}6.{Colors.ENDC} Watch History")
            print(f"{Colors.BOLD}7.{Colors.ENDC} Admin: Manage Movies")
            print(f"{Colors.BOLD}8.{Colors.ENDC} Reports & Statistics")
            print(f"{Colors.BOLD}9.{Colors.ENDC} Logout")
            print(f"{Colors.OKCYAN}{'=' * 50}{Colors.ENDC}")
            
            choice = input_string("Select an option: ")
            
            if choice == '1':
                clear_screen()
                print(f"{Colors.OKCYAN}--- All Movies ---{Colors.ENDC}")
                movie_manager.display_movies()
                
                print("\nOptions:")
                print("1. Watch a Movie (Add to history)")
                print("2. Add to Favorites")
                print("3. Go back")
                sub_choice = input_string("Select option: ")
                if sub_choice == '1':
                    m_id = input_string("Enter Movie ID to watch: ")
                    movie = movie_manager.get_movie_by_id(m_id)
                    if movie:
                        movie_manager.add_to_history(current_user.user_id, m_id)
                        print_success(f"You watched '{movie.title}'!")
                    else:
                        print_error("Invalid Movie ID.")
                elif sub_choice == '2':
                    m_id = input_string("Enter Movie ID to favorite: ")
                    movie_manager.add_favorite(current_user.user_id, m_id)
                pause()
                
            elif choice == '2':
                clear_screen()
                print("1. Search by Title")
                print("2. Search by Category")
                sub = input_string("Choice: ")
                if sub == '1':
                    q = input_string("Enter title: ")
                    movie_manager.search_by_title(q)
                elif sub == '2':
                    q = input_string("Enter category: ")
                    movie_manager.search_by_category(q)
                pause()
                
            elif choice == '3':
                clear_screen()
                recommendation_engine.generate_recommendations(current_user.user_id)
                pause()
                
            elif choice == '4':
                clear_screen()
                movie_manager.display_movies()
                m_id = input_string("\nEnter Movie ID to rate: ")
                score = input_int("Enter rating (1-5): ", 1, 5)
                rating_manager.rate_movie(current_user.user_id, m_id, score)
                pause()
                
            elif choice == '5':
                clear_screen()
                movie_manager.view_favorites(current_user.user_id)
                print("\nOptions:")
                print("1. Remove a favorite")
                print("2. Go back")
                sub = input_string("Select option: ", required=False)
                if sub == '1':
                    m_id = input_string("Enter Movie ID to remove: ")
                    movie_manager.remove_favorite(current_user.user_id, m_id)
                pause()
                
            elif choice == '6':
                clear_screen()
                movie_manager.view_history(current_user.user_id)
                pause()
                
            elif choice == '7':
                clear_screen()
                print(f"{Colors.WARNING}--- ADMIN: Movie Management ---{Colors.ENDC}")
                print("1. Add Movie")
                print("2. Update Movie")
                print("3. Delete Movie")
                print("4. Go back")
                sub = input_string("Select option: ")
                
                if sub == '1':
                    t = input_string("Title: ")
                    c = input_string("Category: ")
                    y = input_int("Year: ")
                    d = input_string("Description: ")
                    movie_manager.add_movie(t, c, y, d)
                elif sub == '2':
                    m_id = input_string("Enter Movie ID to update: ")
                    t = input_string("New Title (leave blank to skip): ", required=False)
                    c = input_string("New Category (leave blank to skip): ", required=False)
                    y_str = input_string("New Year (leave blank to skip): ", required=False)
                    y = int(y_str) if y_str.isdigit() else None
                    d = input_string("New Description (leave blank to skip): ", required=False)
                    movie_manager.update_movie(m_id, t, c, y, d)
                elif sub == '3':
                    m_id = input_string("Enter Movie ID to delete: ")
                    movie_manager.delete_movie(m_id)
                pause()
                
            elif choice == '8':
                clear_screen()
                print(f"{Colors.OKCYAN}--- Reports & Statistics ---{Colors.ENDC}")
                print(f"Total Users: {len(auth_manager.users)}")
                print(f"Total Movies: {len(movie_manager.movies)}")
                print(f"Total Ratings Given: {len(rating_manager.ratings)}")
                
                # Most watched category
                if movie_manager.history:
                    cat_counts = {}
                    for h in movie_manager.history:
                        m = movie_manager.get_movie_by_id(h['movie_id'])
                        if m:
                            cat_counts[m.category] = cat_counts.get(m.category, 0) + 1
                    if cat_counts:
                        best_cat = max(cat_counts, key=cat_counts.get)
                        print(f"Most Watched Category: {best_cat} ({cat_counts[best_cat]} views)")
                
                # Top rated movie
                if movie_manager.movies:
                    top_movie = max(movie_manager.movies, key=lambda m: m.average_rating)
                    if top_movie.average_rating > 0:
                        print(f"Top Rated Movie: {top_movie.title} ({top_movie.average_rating:.1f}/5.0)")
                        
                pause()
                
            elif choice == '9':
                auth_manager.logout()
                pause()
                
            else:
                print_error("Invalid choice. Please try again.")
                pause()

if __name__ == "__main__":
    main()
