function discardDataUntilSymbol(fid, symbol)
% discardDataUntilSymbol(fid, symbol)
% COMMENT ME!
% Read data from fid until finding 'symbol'
%
% (c) MJMJ/2010

while ( fgets(fid,1) ~= symbol)
   if feof(fid)
      break
   end
end