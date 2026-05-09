import argparse
import csv
from tabulate import tabulate


def analyze_youtube_metrics(files, report_name):
    """Анализирует CSV-файлы с метриками YouTube видео"""

    clickbait_videos = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if not all(filed in reader.fieldnames for filed in ['title', 'ctr', 'retention_rate']):
                    print(f"Предупреждение: Файл {file_path} не содержит необходимые колонки")
                    continue

                for row in reader:
                    try:
                        row: dict[str, float]
                        title = row['title']
                        ctr = float(row['ctr'])
                        retention_rate = float(row['retention_rate'])

                        if ctr > 15 and retention_rate < 40:
                            clickbait_videos.append({'title': title, 'ctr': ctr, 'retention_rate': retention_rate})
                    except (ValueError, KeyError) as e:
                        print(f"Ошибка{e}: Файл {file_path} не найден. Пропуск этого файла")
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка при чтении файла {file_path}: {e}")

    clickbait_videos.sort(key=lambda x: x['ctr'], reverse=True)

    if clickbait_videos:
        headers = ["Название видео", "CTR (%)", "Удержание (%)"]
        table_data = [[video['title'], video['ctr'], video['retention_rate']] for video in clickbait_videos]
        print(f"\n ---Отчет: {report_name} ---")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("\nМетрики видео не найдены по заданным критериям.")

    return clickbait_videos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI приложение для анализа метрик YouTube видео.")
    parser.add_argument('--files', nargs='+', required=True, help="Списки CSV-файлов с метриками видео.")
    parser.add_argument('--report', required=True, help="Название отчета.")

    args = parser.parse_args()

    analyze_youtube_metrics(args.files, args.report)
