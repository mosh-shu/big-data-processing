require 'csv'
require 'time'

def getDegree(str) 
    v0 = str[0..1].hex & 0b01111111
    v1 = str[2..3].hex & 0b01111111
    v2 = str[4..5].hex & 0b01111111 
    v3 = str[6..7].hex & 0b01111111
    return ((v0 << 21) | (v1 << 14) | (v2 << 7) | v3) / 60000.0 
end

def getISO8601(str) 
    ye = str[0..1].to_i + 2000 
    mo = str[2..3].to_i 
    da = str[4..5].to_i 
    h = str[8..9].to_i 
    m = str[10..11].to_i 
    s = str[12..13].to_i 
    return sprintf("%04d-%02d-%02dT%02d:%02d:%02d+09:00", ye, mo, da, h, m, s)
end

def putCSV(row)
    csv_string = CSV.generate(:force_quotes=>true){ |csv|
        csv << [getDegree(row[0][0,8]), getDegree(row[0][8,8]), getISO8601(row[0][16,14]), 
                row[0][30,4].hex, row[0][34,4].hex, row[0][38,2].hex, row[0][40,4].to_i,
                row[1].hex, row[2][0,2].hex]
    }
    puts csv_string
end

data = CSV.open(ARGV[0], {:encoding => "Shift_JIS:UTF-8"})

begin
    for row in data
        if row == '\n' or row == '\r'
            next
        else
            putCSV(row)
        end
    end
end