class ScoreProcessor:
    def process_score_file(self, file_path: str) -> int:
        file = None
        try:
            file = open(file_path, 'r')
            content = file.read().strip()
            
            score = int(content)
            result = score * 10
            
        except FileNotFoundError as e:
            print(f"Error: Could not find the file at '{file_path}'.")
            raise e
            
        except ValueError as e:
            print(f"Error: The file '{file_path}' contains invalid data. Expected an integer.")
            raise e
            
        else:
            print("Data processed successfully")
            return result
            
        finally:
            if file is not None:
                file.close()
            print("File cleanup completed")

if __name__ == "__main__":
    processor = ScoreProcessor()

    try:
        result = processor.process_score_file("scorde.txt")
        print(f"Processed Score: {result}")
    except Exception:
        pass